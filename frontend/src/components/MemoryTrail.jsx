// components/MemoryTrail.jsx
import React, { useState, useEffect } from "react";

export default function MemoryTrail({ refresh }) {
  const [memories, setMemories] = useState([]);
  const [show, setShow] = useState(false);

  useEffect(() => {
    const fetchMemories = async () => {
      try {
        const res = await fetch("http://localhost:5000/api/memory");
        const data = await res.json();
        if (Array.isArray(data)) {
          const sorted = data
            .filter((item) => item.query)
            .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
          setMemories(sorted);
        }
      } catch (err) {
        console.error("Failed to load memory:", err);
        setMemories([]);
      }
    };

    fetchMemories();
  }, [refresh]); // ✅ re-fetch whenever refresh changes

  const toggleDropdown = () => setShow(!show);

  return (
    <div className="bg-gray-900 border border-indigo-500 rounded-xl p-3">
      <button
        onClick={toggleDropdown}
        className="w-full text-left text-indigo-300 font-semibold hover:text-indigo-400 transition"
      >
        🧠 Memory Trail {show ? "▲" : "▼"}
      </button>

      {show && (
        <div className="mt-2 max-h-40 overflow-y-auto space-y-1 text-sm text-gray-200">
          {memories.length === 0 ? (
            <p className="text-gray-500">No memories yet.</p>
          ) : (
            memories.map((mem, i) => (
              <div key={i} className="bg-white/5 px-3 py-2 rounded-md">
                <div className="font-medium truncate">
                  📌 {truncateQuery(mem.query)}
                </div>
                <div className="text-xs text-gray-400">
                  {formatTimestamp(mem.timestamp)}
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

function truncateQuery(text, max = 50) {
  return text.length > max ? text.slice(0, max) + "..." : text;
}

function formatTimestamp(timestamp) {
  if (!timestamp) return "";
  const date = new Date(timestamp);
  return date.toLocaleString();
}
