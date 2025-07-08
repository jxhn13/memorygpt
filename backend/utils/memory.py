# utils/memory.py

import os
import json
from difflib import SequenceMatcher

MEMORY_LOG = "chat_memory.json"

def load_memory():
    if os.path.exists(MEMORY_LOG):
        with open(MEMORY_LOG, "r") as f:
            return json.load(f)
    return []

def find_similar_question(new_question, session_id="default", threshold=0.8):
    memory = load_memory()
    for record in reversed(memory):
        if record.get("session_id") != session_id:
            continue
        similarity = SequenceMatcher(None, new_question.lower(), record["query"].lower()).ratio()
        if similarity >= threshold:
            return record
    return None

def save_memory(query, answer, sources):
    memory = load_memory()
    memory.append({
        "query": query,
        "answer": answer,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "sources": sources
    })
    with open(MEMORY_LOG, "w") as f:
        json.dump(memory, f, indent=2)# utils/memory.py

import os
import json
import time  # ✅ Needed for timestamp
from difflib import SequenceMatcher

MEMORY_LOG = "chat_memory.json"

def load_memory():
    if os.path.exists(MEMORY_LOG):
        with open(MEMORY_LOG, "r") as f:
            return json.load(f)
    return []

def find_similar_question(new_question, session_id="default", threshold=0.8):
    memory = load_memory()
    for record in reversed(memory):
        if record.get("session_id") != session_id:
            continue
        similarity = SequenceMatcher(None, new_question.lower(), record["query"].lower()).ratio()
        if similarity >= threshold:
            return record
    return None


def save_memory(query, answer, sources,session_id="default"):
    memory = load_memory()
    memory.append({
        "query": query,
        "answer": answer,
        "sources": sources,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "session_id": session_id
    })
    with open(MEMORY_LOG, "w") as f:
        json.dump(memory, f, indent=2)
def get_last_context(session_id="default"):
    memory = load_memory()
    for record in reversed(memory):
        if record.get("session_id") == session_id:
            return record
    return None
