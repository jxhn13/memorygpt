import React, { useState, useEffect, useRef } from "react";
import Message from "../components/Message";
import UploadPanel from "../components/UploadArea";
import { ChevronDown, ChevronUp } from "lucide-react";
import NeuronPulse from "../components/NeuronPulse";
import MemoryTrail from "../components/MemoryTrail";

export default function Home() {
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState("");
  const [sources, setSources] = useState([]);
  const [uploadedDocs, setUploadedDocs] = useState([]);
  const [showDocs, setShowDocs] = useState(false);
  const [isThinking, setIsThinking] = useState(false);

  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isThinking]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const sendQuery = async () => {
  if (!query.trim()) return;

  const userMessage = { sender: "user", text: query };
  setMessages((prev) => [...prev, userMessage]);
  setQuery("");
  setIsThinking(true);

  try {
    const res = await fetch("http://127.0.0.1:5000/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, history: [] }),
    });

    const data = await res.json();
    const botMessage = { sender: "ai", text: data.response };
    setMessages((prev) => [...prev, botMessage]);
    setSources(data.sources || []);
    setMemoryRefreshFlag((prev) => prev + 1); // ✅ Trigger MemoryTrail reload
  } catch (err) {
    console.error("Chat error:", err);
  } finally {
    setIsThinking(false);
  }
};

  const handleUploadComplete = (docs) => {
    setUploadedDocs((prev) => [...prev, ...docs]);
  };

  const handleDelete = async (filename) => {
    try {
      const res = await fetch("http://localhost:5000/api/delete-file", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ filename }),
      });

      if (res.ok) {
        setUploadedDocs((prev) => prev.filter((doc) => doc.name !== filename));
      } else {
        const err = await res.json();
        alert(err.error || "Failed to delete.");
      }
    } catch (err) {
      console.error(err);
      alert("Something went wrong.");
    }
  };
  const handleMemoryClear = async () => {
  try {
    const res = await fetch("http://localhost:5000/api/clear-memory", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });

    if (res.ok) {
      alert("Memory trail cleared successfully.");
    } else {
      const err = await res.json();
      alert(err.error || "Failed to clear memory.");
    }
  } catch (err) {
    console.error(err);
    alert("Something went wrong while clearing memory.");
  }
};


  return (
    <div className="min-h-screen w-full flex flex-col bg-gradient-to-br from-gray-950 to-black text-white overflow-hidden relative">
      
      {/* Header */}
      <header className="py-6">
        <h1 className="text-center text-5xl font-extrabold tracking-wide relative z-10">
          <span className="animate-textPulse bg-gradient-to-r from-[#00ffe0] via-[#a855f7] to-[#ff2eaa] bg-clip-text text-transparent drop-shadow-[0_0_10px_rgba(255,255,255,0.3)]">
            🧠Memory
          </span>
          <span className="ml-2 text-yellow-400 drop-shadow-[0_0_10px_rgba(255,255,0,0.6)] animate-glowText">
            GPT
          </span>
        </h1>
        <p className="text-center mt-2 text-gray-400 text-sm">Where your queries live forever 🧠</p>
      </header>

      {/* Uploaded Docs Dropdown */}
      <div className="absolute right-6 top-6 z-30">
        <button
          onClick={() => setShowDocs(!showDocs)}
          className="flex items-center gap-2 text-sm px-4 py-2 rounded-full bg-black/50 border border-white/10 backdrop-blur-md text-white hover:bg-black/70"
        >
          {showDocs ? "Hide Docs" : "Show Docs"}
          {showDocs ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
        </button>

        {showDocs && (
          <div className="mt-2 bg-black/60 rounded-xl p-4 max-w-sm w-[300px] text-sm text-white border border-gray-600 shadow-xl space-y-4">
            <div>
              <p className="font-semibold text-indigo-400 mb-2">📁 Uploaded Files:</p>
              {uploadedDocs.length === 0 ? (
                <p className="text-gray-400">No files uploaded yet.</p>
              ) : (
                uploadedDocs.map((doc) => (
                  <div key={doc.name} className="bg-white/5 rounded-lg px-3 py-2 mb-2">
                    <div className="flex justify-between items-center">
                      <div>
                        <div className="truncate font-medium">{doc.name}</div>
                        <div className="text-xs text-gray-400">
                          📄 {doc.size} KB • ⏱ {doc.time}
                        </div>
                      </div>
                      <button
                        className="text-red-500 text-sm ml-4 hover:underline"
                        onClick={() => handleDelete(doc.name)}
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>

            {/* Memory Trail Section */}
           <div className="mt-4 flex items-center justify-between text-xs text-white/80">
  <div className="truncate max-w-[200px]">
    <MemoryTrail />
  </div>
  <button
    onClick={handleMemoryClear}
    className="ml-4 text-red-400 hover:text-red-300 hover:underline transition-all"
  >
    Clear
  </button>
</div>



          </div>
        )}
      </div>

      {/* Chat Messages */}
      <main className="flex-1 overflow-y-auto px-4 pb-40 md:px-16 scroll-smooth">
  <div className="max-w-6xl mx-auto space-y-6">

          {messages.map((msg, idx) => (
            <Message key={idx} sender={msg.sender} text={msg.text} />
          ))}
          {isThinking && <NeuronPulse />}
          <div ref={bottomRef} />
        </div>
      </main>

      {/* Bottom Bar */}
      <div className="fixed bottom-0 left-0 right-0 z-20 bg-black/80 backdrop-blur-md border-t border-gray-800 px-4 py-4 flex flex-col md:flex-row items-center gap-3">
        <input
          ref={inputRef}
          type="text"
          className="flex-1 w-full px-5 py-3 rounded-full bg-gray-900 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 text-white placeholder-gray-400"
          placeholder="Ask MemoryGPT something..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendQuery()}
          disabled={isThinking}
        />
        <button
          onClick={sendQuery}
          className={`px-6 py-2 rounded-full ${
            isThinking ? "bg-blue-400 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"
          } text-white font-semibold transition-all duration-300`}
          disabled={isThinking}
        >
          {isThinking ? "Thinking..." : "Ask"}
        </button>
        <UploadPanel onComplete={handleUploadComplete} />
      </div>
    </div>
  );
}
