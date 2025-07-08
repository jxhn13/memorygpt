from datetime import datetime

def enrich_metadata(chunk, source):
    return {
        "source": source,
        "timestamp": datetime.now().isoformat(),
        "chunk_id": hash(chunk.page_content[:100])
    }
