import os
import json
from datetime import datetime

MEMORY_LOG = "chat_memory.json"

# 🔹 Ensure memory file exists
def ensure_memory_log():
    if not os.path.exists(MEMORY_LOG):
        with open(MEMORY_LOG, "w") as f:
            json.dump([], f)

# 🔹 Save chat interaction (per session)
def save_chat_history(query, answer, sources=None, session_id="default"):
    ensure_memory_log()

    new_entry = {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "answer": answer,
        "sources": sources or []
    }

    try:
        with open(MEMORY_LOG, "r") as f:
            data = json.load(f)

        data.append(new_entry)

        with open(MEMORY_LOG, "w") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print(f"❌ Error saving memory: {e}")

# 🔹 Find similar question in session
def find_similar_question(new_query, session_id="default"):
    ensure_memory_log()

    try:
        with open(MEMORY_LOG, "r") as f:
            data = json.load(f)

        # Simple match (you can replace with semantic match)
        for item in reversed(data):
            if item["session_id"] == session_id and item["query"].lower() == new_query.lower():
                return item

        return None

    except Exception as e:
        print(f"❌ Error searching memory: {e}")
        return None

# 🔹 Get last context (for UI display or follow-up)
def get_last_context(session_id="default"):
    ensure_memory_log()

    try:
        with open(MEMORY_LOG, "r") as f:
            data = json.load(f)

        session_data = [item for item in data if item["session_id"] == session_id]
        return session_data[-1] if session_data else {}

    except Exception as e:
        print(f"❌ Error retrieving context: {e}")
        return {}
