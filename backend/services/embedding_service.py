import os
from langchain_community.vectorstores import FAISS
from langchain_cohere import CohereEmbeddings
from config import config

import cohere

co = cohere.Client(os.getenv("COHERE_API_KEY"))


embedding_model = CohereEmbeddings(
    model=config.EMBEDDING_MODEL,
    cohere_api_key=os.getenv("COHERE_API_KEY")
)

# ✅ Tag extractor
def extract_tags(text):
    prompt = (
        "Extract important named entities or tags from the text below. "
        "Tags can include names of people, companies, technologies, locations, products, or events. "
        "Return only a comma-separated list of tags.\n\n"
        f"Text: {text}\n\nTags:"
    )

    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=60,
        temperature=0.3,
    )

    raw_output = response.generations[0].text.strip()
    tags = [tag.strip() for tag in raw_output.split(",") if tag.strip()]
    return list(set(tags))

# ✅ Load existing FAISS index (used for querying)
def load_vectorstore():
    path = config.VECTORSTORE_PATH
    faiss_file = os.path.join(path, "index.faiss")
    meta_file = os.path.join(path, "index.pkl")

    if os.path.exists(faiss_file) and os.path.exists(meta_file):
        print("✅ Vectorstore found and loaded.")
        return FAISS.load_local(path, embedding_model, allow_dangerous_deserialization=True)
    else:
        print("⚠️ Vectorstore files not found.")
        return None

def get_vectorstore(docs):
    path = config.VECTORSTORE_PATH
    faiss_file = os.path.join(path, "index.faiss")

    os.makedirs(path, exist_ok=True)

    if os.path.exists(faiss_file):
        index = FAISS.load_local(path, embedding_model, allow_dangerous_deserialization=True)
        new_index = FAISS.from_documents(docs, embedding_model)
        index.merge_from(new_index)
    else:
        index = FAISS.from_documents(docs, embedding_model)

    index.save_local(path)
    return index

# ✅ Embed and store new docs with metadata
def embed_and_store(documents, metadata):
    if not documents:
        print("⚠️ No documents to embed.")
        return None

    new_docs = []
    for doc in documents:
        if not hasattr(doc, "page_content") or not doc.page_content.strip():
            continue

        tags = extract_tags(doc.page_content)
        doc.metadata.update(metadata)
        doc.metadata["tags"] = tags
        new_docs.append(doc)

    if not new_docs:
        print("⚠️ No valid documents to embed.")
        return None

    get_vectorstore(new_docs)
    print(f"✅ {len(new_docs)} documents embedded and FAISS vectorstore updated.")
