import re

def clean_text(text: str) -> str:
    """
    Removes excessive whitespace, non-ASCII characters, etc.
    """
    text = text.encode("ascii", errors="ignore").decode()
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def allowed_file(filename, allowed_extensions):
    """
    Checks if file is an allowed upload type.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def summarize_metadata(doc):
    """
    Returns a compact summary of doc metadata for logging/UI.
    """
    source = doc.metadata.get("source", "unknown")
    page = doc.metadata.get("page", "N/A")
    timestamp = doc.metadata.get("timestamp", "N/A")
    return f"{source} (Page: {page}, Time: {timestamp})"
def is_visual_query(text):
    keywords = ["chart", "graph", "plot", "visualize", "draw"]
    return any(kw in text.lower() for kw in keywords)
