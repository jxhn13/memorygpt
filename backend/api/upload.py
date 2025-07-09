from flask import Blueprint, request, jsonify
import os, time
from werkzeug.utils import secure_filename
from config import config
from services.filehandler import parse_document
from services.embedding_service import embed_and_store

upload_bp = Blueprint("upload", __name__)

# (Optional) allowed extensions
# ALLOWED_EXTENSIONS = {"pdf", "txt", "docx"}
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route("/upload", methods=["POST"])
def upload_files():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        files = request.files.getlist("file")
        if not files or files[0].filename == "":
            return jsonify({"error": "No files selected"}), 400

        all_chunks = []
        uploaded_files_info = []

        os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists

        for file in files:
            filename = secure_filename(file.filename)

            # (Optional): skip invalid file types
            # if not allowed_file(filename):
            #     continue

            filepath = os.path.join(config.UPLOAD_FOLDER, filename)
            file.save(filepath)

            # ✅ Parse and chunk
            doc_chunks = parse_document(filepath)
            if not doc_chunks:
                continue

            for chunk in doc_chunks:
                chunk.metadata["source"] = filename

            all_chunks.extend(doc_chunks)

            # ✅ Add file details for UI
            file.seek(0, os.SEEK_END)
            size_kb = round(file.tell() / 1024, 2)
            uploaded_files_info.append({
                "name": filename,
                "size": size_kb,
                "time": time.strftime("%I:%M %p")
            })

        if not all_chunks:
            return jsonify({"error": "❌ No valid document chunks to embed."}), 400

        embed_and_store(all_chunks, metadata={"source": filename})


        return jsonify({
            "message": f"✅ {len(uploaded_files_info)} file(s) uploaded and embedded successfully.",
            "files": uploaded_files_info
        }), 200

    except Exception as e:
        return jsonify({"error": f"🔥 Upload failed: {str(e)}"}), 500
