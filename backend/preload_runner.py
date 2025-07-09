import os
from services.filehandler import parse_document
from services.embedding_service import embed_and_store

DEFAULT_FOLDER = "static/default_docs"

def preload_documents(folder=DEFAULT_FOLDER):
    print(f"📂 Preloading documents from: {folder}")
    all_chunks = []

    if not os.path.exists(folder):
        print("❌ No default folder found.")
        return

    for filename in os.listdir(folder):
        if filename.endswith((".pdf", ".txt", ".docx")):
            filepath = os.path.join(folder, filename)
            print(f"🔍 Parsing: {filename}")
            chunks = parse_document(filepath)

            # Add filename to metadata
            for chunk in chunks:
                chunk.metadata["source"] = filename

            all_chunks.extend(chunks)

    if all_chunks:
        embed_and_store(all_chunks)
        print(f"✅ {len(all_chunks)} chunks embedded and stored in FAISS.")
    else:
        print("⚠️ No valid chunks found during preload.")

if __name__ == "__main__":
    print("🚀 Starting MemoryGPT document preload...")
    preload_documents()
    print("✅ Preload completed.")
