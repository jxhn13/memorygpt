import os
from config import config
from langchain_community.vectorstores import FAISS
from langchain_cohere import CohereEmbeddings
from langchain.schema import Document
from keybert import KeyBERT

kw_model = KeyBERT()

# ✅ Setup embedding model with Cohere (only for vector embedding)
embedding_model = CohereEmbeddings(
    model=config.EMBEDDING_MODEL,  # e.g., "embed-english-light-v3.0"
    cohere_api_key=os.getenv("COHERE_API_KEY")
)

# ✅ Local tag extraction using KeyBERT
def extract_tags(text: str) -> list[str]:
    try:
        keywords = kw_model.extract_keywords(text, top_n=5)
        return [kw for kw, _ in keywords]
    except Exception as e:
        print("❌ Local tag extraction failed:", e)
        return []

# ✅ Load vectorstore from disk
def load_vectorstore():
    path = config.VECTORSTORE_PATH
    if os.path.exists(os.path.join(path, "index.faiss")) and os.path.exists(os.path.join(path, "index.pkl")):
        print("✅ Vectorstore loaded.")
        return FAISS.load_local(path, embedding_model, allow_dangerous_deserialization=True)
    print("⚠️ No vectorstore found.")
    return None

# ✅ Create or update vectorstore
def get_vectorstore(documents: list[Document]):
    path = config.VECTORSTORE_PATH
    os.makedirs(path, exist_ok=True)

    faiss_exists = os.path.exists(os.path.join(path, "index.faiss"))

    if faiss_exists:
        index = FAISS.load_local(path, embedding_model, allow_dangerous_deserialization=True)
        new_index = FAISS.from_documents(documents, embedding_model)
        index.merge_from(new_index)
    else:
        index = FAISS.from_documents(documents, embedding_model)

    index.save_local(path)
    return index

# ✅ Embed and store documents with metadata + tags
def embed_and_store(documents: list[Document], metadata: dict = {}):
    if not documents:
        print("⚠️ No documents to embed.")
        return

    valid_docs = []
    for doc in documents:
        content = getattr(doc, "page_content", "").strip()
        if not content:
            continue

        tags = extract_tags(content)
        doc.metadata.update(metadata)
        doc.metadata["tags"] = tags
        valid_docs.append(doc)

    if not valid_docs:
        print("⚠️ No valid chunks to embed.")
        return

    get_vectorstore(valid_docs)
    print(f"✅ {len(valid_docs)} documents embedded and stored in FAISS.")
