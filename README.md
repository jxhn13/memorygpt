
# 🧠 MemoryGPT

A conversational memory-augmented AI system that allows users to upload documents and query them in real-time — where your queries live forever.

---



## 🛠 Tech Stack

- **Frontend:** React.js, Tailwind CSS, Lucide Icons
- **Backend:** Flask, LangChain, FAISS, Cohere/OpenAI embeddings
- **Vector Store:** FAISS (stored locally)
- **PDF Parsing:** PyMuPDF, Unstructured
- **Deployment:** Vercel (Frontend), Render (Backend)

---

## 📦 Installation

### 🔧 Backend Setup

```bash
# Clone the repository
git clone https://github.com/jxhn13/memorygpt.git
cd memorygpt/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows

# Install requirements
pip install -r requirements.txt
````

Create a `.env` file:

```env
COHERE_API_KEY=your_cohere_api_key
# or
OPENAI_API_KEY=your_openai_api_key
EMBEDDING_MODEL=embed-english-light-v3.0
```

---

### 💻 Frontend Setup

```bash
cd ../frontend
npm install
npm run dev  # Runs on http://localhost:5173
```

Update `API_BASE` in `src/Pages/Home.jsx`:

```js
const API_BASE = "http://localhost:5000"; // For local
// Or use Render URL in production
```

---

## 🧠 Features

* 📁 Upload PDFs, DOCX, and TXT files
* 🔍 Ask contextual questions from documents
* 🧩 Visual memory trail of chat history
* 📌 Persistent vector store (FAISS)
* 🎯 Tag extraction using KeyBERT
* 🚫 Memory clearing and file deletion
* ✨ Immersive UI with animated chat

---

## 🧪 API Endpoints

| Method | Endpoint            | Description             |
| ------ | ------------------- | ----------------------- |
| POST   | `/api/chat`         | Query with question     |
| POST   | `/api/upload`       | Upload a document       |
| POST   | `/api/delete-file`  | Delete uploaded file    |
| POST   | `/api/clear-memory` | Clear all stored memory |
| GET    | `/`                 | Health check route      |

---

## ⚙️ Deployment

### Render (Backend)

1. Create a new **Web Service**
2. Add build command: `pip install -r requirements.txt`
3. Start command: `python app.py`
4. Add environment variable: `PORT = 10000`, `COHERE_API_KEY`, etc.
5. Make sure `vector_store/` is committed if you skip preloading

### Vercel (Frontend)

1. Link GitHub repo to Vercel
2. Set `VITE_API_BASE` in Vercel Dashboard
3. Deploy 🚀

---

## 📁 Folder Structure

```
memorygpt/
├── backend/
│   ├── api/              # Flask API routes
│   ├── services/         # RAG logic, embedding, file handling
│   ├── utils/            # Helpers and memory functions
│   ├── vector_store/     # FAISS index files
│   ├── app.py            # Main backend app
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── public/
│   └── vite.config.js
```

---

## 🙋‍♂️ Author

**John Shajan**
GitHub: [@jxhn13](https://github.com/jxhn13)
LinkedIn: [linkedin.com/in/johnshajan](https://linkedin.com/in/johnshajan)

---

## ⚖️ License

This project is licensed under the [MIT License](LICENSE).

````




