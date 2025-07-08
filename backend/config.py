import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    PROVIDER = os.getenv("LLM_PROVIDER", "cohere")  # default to cohere
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")

    # Set these conditionally based on provider
    if PROVIDER == "openai":
        EMBEDDING_MODEL = "text-embedding-ada-002"
        CHAT_MODEL = "gpt-4"
    elif PROVIDER == "cohere":
        EMBEDDING_MODEL = "embed-english-v3.0"
        CHAT_MODEL = "command-r-plus"  # or other available Cohere chat models

    VECTORSTORE_PATH = "vector_store/faiss_index"
    UPLOAD_FOLDER = "./uploads"
    ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

config = Config()
