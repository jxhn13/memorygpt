// src/components/SourceCard.jsx
import React from "react";

export default function SourceCard({ source, page, snippet, tags = [] }) {
  return (
    <div className="bg-gray-900 border border-gray-700 rounded-xl p-4 my-2 text-sm">
      <p className="mb-2 text-gray-300">
        📄 <strong>{source}</strong> — page {page ?? "?"}
      </p>
      <p className="text-gray-400 italic">“{snippet}...”</p>
      {tags.length > 0 && (
        <div className="mt-2 flex flex-wrap gap-2">
          {tags.map((tag, i) => (
            <span
              key={i}
              className="bg-blue-800 text-xs text-white px-2 py-1 rounded-full"
            >
              #{tag}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
