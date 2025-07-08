export default function Message({ sender, text }) {
  const isUser = sender === "user";

  return (
    <div className={`w-full flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[70%] px-4 py-3 rounded-xl shadow-md whitespace-pre-line 
        ${isUser ? "bg-blue-600 text-white rounded-br-none" : "bg-gray-800 text-white rounded-bl-none"}`}
      >
        {text}
        
      </div>
    </div>
  );
}
