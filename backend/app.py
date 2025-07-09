from flask import Flask
from flask_cors import CORS
from api.upload import upload_bp
from api.chat import chat_bp
import os

# ✅ Optional Preload Utilities
from services.filehandler import parse_document
from services.embedding_service import embed_and_store

def preload_documents(folder="static/default_docs"):
    print("📂 Preloading documents from:", folder)
    all_chunks = []

    if not os.path.exists(folder):
        print("❌ No default folder found.")
        return

    for filename in os.listdir(folder):
        if filename.endswith((".pdf", ".txt", ".docx")):
            filepath = os.path.join(folder, filename)
            print(f"🔍 Parsing: {filename}")
            chunks = parse_document(filepath)
            for chunk in chunks:
                chunk.metadata["source"] = filename
            all_chunks.extend(chunks)

    if all_chunks:
        embed_and_store(all_chunks)
        print(f"✅ {len(all_chunks)} chunks embedded from default documents.")
    else:
        print("⚠️ No valid chunks found during preload.")

# ✅ Flask App
app = Flask(__name__)
CORS(app, origins=["https://memorygpt.vercel.app"])


# Register blueprints
app.register_blueprint(upload_bp, url_prefix="/api")
app.register_blueprint(chat_bp, url_prefix="/api")

@app.route("/")
def index():
    return {"message": "MemoryGPT Backend is running"}

if __name__ == "__main__":
    from waitress import serve
    preload_documents()
    port = int(os.environ.get("PORT", 5000))
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Flask side
    serve(app, host="0.0.0.0", port=port, max_request_body_size=1024*1024*100)  # Waitress side


