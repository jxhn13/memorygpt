import os
import json

CHAT_HISTORY_FILE = "chat_memory.json"

def save_chat_history(question, answer):
    history = []
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r") as f:
            history = json.load(f)

    history.append({"question": question, "answer": answer})

    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)