from flask import Flask
from flask_cors import CORS
from api.upload import upload_bp
from api.chat import chat_bp
import os

# ✅ Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["https://memorygpt.vercel.app"])  # For production deployment

# ✅ Register routes
app.register_blueprint(upload_bp, url_prefix="/api")
app.register_blueprint(chat_bp, url_prefix="/api")

# ✅ Health check route
@app.route("/")
def index():
    return {"message": "MemoryGPT Backend is running"}

# ✅ Start the app using waitress
if __name__ == "__main__":
    from waitress import serve
    port = int(os.environ.get("PORT", 5000))
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Limit uploads to 100MB
    print(f"🚀 Starting MemoryGPT backend on port {port}...")
    serve(app, host="0.0.0.0", port=port)
