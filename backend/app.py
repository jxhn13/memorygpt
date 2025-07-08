from flask import Flask
from flask_cors import CORS  # ✅ Import CORS
from api.upload import upload_bp
from api.chat import chat_bp
import os
app = Flask(__name__)
CORS(app, origins=["https://memorygpt.vercel.app"])

# Register blueprints
app.register_blueprint(upload_bp, url_prefix="/api")
app.register_blueprint(chat_bp, url_prefix="/api")

@app.route("/")
def index():
    return {"message": "MemoryGPT Backend is running"}



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

