import React, { useState } from "react";
import { UploadCloud, Loader2 } from "lucide-react";

export default function UploadPanel({ onComplete }) {
  const [uploading, setUploading] = useState(false);

  const handleFileChange = async (e) => {
    const files = Array.from(e.target.files);
    if (!files.length) return;

    setUploading(true);
    const formData = new FormData();
    files.forEach((f) => formData.append("file", f));

    try {
      const res = await fetch("http://127.0.0.1:5000/api/upload", {
        method: "POST",
        body: formData,
      });

      if (res.ok) {
        const docs = files.map((f) => ({
          name: f.name,
          size: (f.size / 1024).toFixed(1),
          time: new Date().toLocaleTimeString(),
        }));
        onComplete(docs);
      }
    } catch (err) {
      console.error("Upload failed", err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <label className="cursor-pointer text-sm px-4 py-2 bg-black/60 border border-white/10 rounded-full hover:bg-black/80 text-white transition">
      {uploading ? (
        <span className="flex items-center gap-2">
          <Loader2 className="animate-spin w-4 h-4" />
          Uploading...
        </span>
      ) : (
        <span className="flex items-center gap-2">
          <UploadCloud size={16} /> Upload
        </span>
      )}
      <input
        type="file"
        multiple
        className="hidden"
        onChange={handleFileChange}
      />
    </label>
  );
}
