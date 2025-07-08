// src/components/NeuronPulse.jsx
import React from "react";

export default function NeuronPulse() {
  return (
    <div className="flex justify-start">
      <div className="bg-gray-800 px-4 py-3 rounded-xl shadow-md border border-gray-700">
        <div className="flex space-x-2 items-center">
          <div className="w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
          <div className="w-2 h-2 rounded-full bg-purple-500 animate-pulse delay-100" />
          <div className="w-2 h-2 rounded-full bg-pink-500 animate-pulse delay-200" />
          <span className="ml-2 text-sm text-gray-300">Thinking...</span>
        </div>
      </div>
    </div>
  );
}
