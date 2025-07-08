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

# 🔹 RAG Chat Endpoint
@chat_bp.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        query = data.get("query", "")
        chat_history = data.get("history", [])
        session_id = data.get("session_id", "default")

        if not query:
            return jsonify({"error": "Query is required"}), 400

        # 🧠 Check for similar past question
        past = find_similar_question(query, session_id)
        if past:
            return jsonify({
                "response": f"🧠 You asked a similar question before:\nQ: {past['query']}\nA: {past['answer']}",
                "sources": past.get("sources", [])
            })

        # 🔍 Get answer from RAG pipeline
        result = answer_query(query, chat_history)

        if not result or "answer" not in result:
            return jsonify({"response": "⚠️ No answer could be generated.", "sources": []}), 500

        # 📁 Prepare sources
        sources = []
        for doc in result.get("source_documents", []):
            sources.append({
                "source": doc.metadata.get("source", "unknown"),
                "page": doc.metadata.get("page", None),
                "snippet": doc.page_content[:200],
                "tags": doc.metadata.get("tags", [])
            })

        # 💾 Save memory
        save_memory(query, result.get("answer"), sources, session_id=session_id)
        get_last_context(session_id=session_id)

        # 📊 Return chart if visual query
        if is_visual_query(query):
            structured_data = result.get("chart_data", {})
            image_base64 = plot_chart(structured_data)
            return jsonify({
                "response": "Here's your visualization",
                "chart": image_base64,
                "sources": sources,
                "type": "visual"
            })

        # 📝 Return text response
        return jsonify({
            "response": result.get("answer"),
            "sources": sources,
            "type": "text"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🧠 Memory Trail Fetch Endpoint
@chat_bp.route("/memory", methods=["GET"])
def get_memory():
    if not os.path.exists(MEMORY_LOG):
        return jsonify([])

    try:
        with open(MEMORY_LOG, "r") as f:
            memory_data = json.load(f)
            return jsonify(memory_data)
    except json.JSONDecodeError:
        return jsonify([])


# 🗑 Clear Memory Endpoint
@chat_bp.route("/clear-memory", methods=["POST"])
def clear_memory():
    try:
        with open(MEMORY_LOG, "w") as f:
            f.write("[]")
        return jsonify({"message": "Memory trail cleared."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🗃 Delete Uploaded File Endpoint
@chat_bp.route("/delete-file", methods=["POST"])
def delete_file():
    data = request.get_json()
    filename = data.get("filename")

    if not filename:
        return jsonify({"error": "Filename required"}), 400

    filepath = os.path.join(config.UPLOAD_FOLDER, filename)

    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({"message": f"{filename} deleted successfully."}), 200
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
