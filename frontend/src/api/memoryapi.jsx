// src/api/memoryAPI.jsx

const BASE_URL = "http://127.0.0.1:5000/api";

export async function sendQueryToMemoryGPT(query, history = [], session_id = "default") {
  try {
    const response = await fetch(`${BASE_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query,
        history,
        session_id,
      }),
    });

    if (!response.ok) {
      throw new Error(`❌ API error: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("🧠 Query Error:", error);
    return {
      response: "⚠️ Something went wrong. Please try again.",
      sources: [],
    };
  }
}

export async function uploadFilesToMemoryGPT(formData) {
  try {
    const response = await fetch(`${BASE_URL}/upload`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`❌ Upload failed: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("📁 Upload Error:", error);
    return { message: "⚠️ Upload failed. Try again." };
  }
}
