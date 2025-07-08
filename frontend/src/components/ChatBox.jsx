// src/components/ChatBox.jsx
import React, { useState } from "react";
import axios from "axios";

export default function ChatBox() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [sources, setSources] = useState([]);

  const sendQuery = async () => {
  if (!query.trim()) return;

  const userMessage = { sender: "user", text: query };
  setMessages((prev) => [...prev, userMessage]);
  setQuery("");
  setIsThinking(true);  // show neuron animation

  try {
    const res = await fetch("http://127.0.0.1:5000/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, history: [] }),
    });

    const data = await res.json();
    const botMessage = { sender: "ai", text: data.response,
  chart: data.chart || null, };
    setMessages((prev) => [...prev, botMessage]);
  } catch (err) {
    setMessages((prev) => [...prev, { sender: "ai", text: "⚠️ Something went wrong." }]);
  } finally {
    setIsThinking(false);  // hide animation
  }
};


  return (
    <div className="bg-white bg-opacity-10 p-4 rounded-xl shadow-lg h-full">
      <h2 className="text-xl font-semibold mb-4">💬 Ask MemoryGPT</h2>
      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        rows="4"
        className="w-full p-2 rounded bg-gray-800 text-white mb-4"
        placeholder="Ask a question..."
      />
      <button onClick={sendQuery} className="px-4 py-2 bg-green-600 hover:bg-green-700 rounded text-white">
        Ask
      </button>
      <div className="mt-6">
        <h3 className="font-bold">Response:</h3>
        <p className="text-sm mt-2">{response}</p>
        {sources.length > 0 && (
          <div className="mt-4">
            <h4 className="font-semibold">Sources:</h4>
            <ul className="text-xs list-disc pl-6">
              {sources.map((src, idx) => (
                <li key={idx}>{src.source} (p.{src.page})</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
