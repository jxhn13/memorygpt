import os
import json
from langchain_community.document_loaders import (
    PyMuPDFLoader,
    TextLoader,
    Docx2txtLoader,
    UnstructuredHTMLLoader,
    CSVLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

def parse_document(filepath):
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":
        loader = PyMuPDFLoader(filepath)
    elif ext == ".txt":
        loader = TextLoader(filepath, encoding="utf-8")
    elif ext == ".docx":
        loader = Docx2txtLoader(filepath)
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
    return splitter.split_documents(documents)

def load_json_as_documents(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    content = json.dumps(data, indent=2)
    return [Document(page_content=content)]
