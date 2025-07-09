from flask import Blueprint, request, jsonify
from services.rag import answer_query
from services.visualizer import plot_chart
from utils.helpers import is_visual_query
from utils.memory import save_memory, find_similar_question, get_last_context
from config import config

import json
import os

chat_bp = Blueprint("chat", __name__)
MEMORY_LOG = "chat_memory.json"

# 🔹 Chat API with RAG + Memory
@chat_bp.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        query = data.get("query", "").strip()
        chat_history = data.get("history", [])
        session_id = data.get("session_id", "default")

        if not query:
            return jsonify({"error": "Query is required"}), 400

        # 🧠 Check for similar past queries
        past = find_similar_question(query, session_id)
        if past:
            return jsonify({
                "response": f"🧠 You asked a similar question before:\nQ: {past['query']}\nA: {past['answer']}",
                "sources": past.get("sources", []),
                "type": "memory"
            })

        # 🔍 Run RAG pipeline
        result = answer_query(query, chat_history)

        if not result or "answer" not in result:
            return jsonify({"response": "⚠️ No answer could be generated.", "sources": []}), 500

        # 📄 Format sources
        sources = [
            {
                "source": doc.metadata.get("source", "unknown"),
                "page": doc.metadata.get("page", None),
                "snippet": doc.page_content[:200],
                "tags": doc.metadata.get("tags", [])
            }
            for doc in result.get("source_documents", [])
        ]

        # 💾 Save to memory
        save_memory(query, result["answer"], sources, session_id=session_id)
        get_last_context(session_id=session_id)

        # 📊 If visual query
        if is_visual_query(query):
            chart_data = result.get("chart_data", {})
            image_base64 = plot_chart(chart_data)
            return jsonify({
                "response": "📊 Here's your visualization.",
                "chart": image_base64,
                "sources": sources,
                "type": "visual"
            })

        # 📝 Text response
        return jsonify({
            "response": result["answer"],
            "sources": sources,
            "type": "text"
        })

    except Exception as e:
        print(f"🔥 Chat error: {e}")
        return jsonify({"error": str(e)}), 500


# 🧠 Get Memory Trail
@chat_bp.route("/memory", methods=["GET"])
def get_memory():
    try:
        if not os.path.exists(MEMORY_LOG):
            return jsonify([])
        with open(MEMORY_LOG, "r") as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🧹 Clear Memory
@chat_bp.route("/clear-memory", methods=["POST"])
def clear_memory():
    try:
        with open(MEMORY_LOG, "w") as f:
            f.write("[]")
        return jsonify({"message": "✅ Memory trail cleared."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🗃 Delete Uploaded File
@chat_bp.route("/delete-file", methods=["POST"])
def delete_file():
    try:
        data = request.get_json()
        filename = data.get("filename", "").strip()

        if not filename:
            return jsonify({"error": "Filename is required"}), 400

        filepath = os.path.join(config.UPLOAD_FOLDER, filename)

        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({"message": f"✅ {filename} deleted successfully."})
        else:
            return jsonify({"error": "❌ File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
