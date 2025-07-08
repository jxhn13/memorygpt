import os
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredHTMLLoader,
    CSVLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json

def parse_document(filepath):
    ext = os.path.splitext(filepath)[1].lower()

    # Select appropriate loader
    if ext == ".pdf":
        loader = PyPDFLoader(filepath)
    elif ext == ".txt":
        loader = TextLoader(filepath, encoding="utf-8")
    elif ext == ".docx":
        loader = UnstructuredWordDocumentLoader(filepath)
    elif ext == ".csv":
        loader = CSVLoader(filepath)
    elif ext == ".md":
        loader = TextLoader(filepath, encoding="utf-8")
    elif ext == ".html":
        loader = UnstructuredHTMLLoader(filepath)
    elif ext == ".json":
        return load_json_as_documents(filepath)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    documents = loader.load()

    # Chunk into smaller pieces
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    return splitter.split_documents(documents)

# Optional: custom JSON handler
def load_json_as_documents(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Flatten into a single string for now
    content = json.dumps(data, indent=2)
    from langchain.schema import Document
    return [Document(page_content=content)]
