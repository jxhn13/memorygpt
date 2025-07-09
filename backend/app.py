from flask import Flask
from flask_cors import CORS
from api.upload import upload_bp
from api.chat import chat_bp
import os

# ✅ Optional Preload Utilities (if needed)
# from services.filehandler import parse_document
# from services.embedding_service import embed_and_store

# def preload_documents(folder="static/default_docs"):
#     # Optional preload logic (disabled if you're pushing vectorstore)
#     pass

app = Flask(__name__)
CORS(app, origins=["https://memorygpt.vercel.app"])

# Register routes
app.register_blueprint(upload_bp, url_prefix="/api")
app.register_blueprint(chat_bp, url_prefix="/api")

@app.route("/")
def index():
    return {"message": "MemoryGPT Backend is running"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render provides PORT
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
    print(f"🚀 Starting MemoryGPT backend on port {port}...")
    app.run(host="0.0.0.0", port=port)
