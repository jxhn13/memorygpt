import os
import cohere
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from services.embedding_service import load_vectorstore
from config import config
from services.chatmem import save_chat_history

# 🔹 Cohere setup
co = cohere.Client(os.getenv("COHERE_API_KEY"))

from langchain.llms.base import LLM
from typing import Optional, List
from pydantic import Extra

# 🔹 Custom LLM wrapper for Cohere
class CohereLLM(LLM):
    model: str = "command"
    temperature: float = 0.5
    max_tokens: int = 300

    class Config:
        extra = Extra.forbid

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = co.generate(
            model=self.model,
            prompt=prompt,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        return response.generations[0].text.strip()

    @property
    def _llm_type(self) -> str:
        return "cohere"

# ✅ Initialize the LLM
llm = CohereLLM()

# ✅ Load vectorstore (used only for retrieval)
vectorstore = load_vectorstore()
retriever = None

if vectorstore:
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )
else:
    print("⚠️ Vectorstore not found. Please upload documents first.")

# ✅ Chat memory buffer
memory = ConversationBufferMemory(
    return_messages=True,
    input_key="question",
    output_key="answer"
)

# ✅ Build the conversational retrieval chain
qa_chain = None
if retriever:
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True
    )
else:
    print("⚠️ QA Chain not initialized due to missing retriever.")

# ✅ Main query interface
from services.embedding_service import load_vectorstore

def answer_query(query, chat_history=[]):
    # ✅ Always load the latest FAISS index
    vectorstore = load_vectorstore()
    if not vectorstore:
        return {
            "answer": "⚠️ Retrieval not available. Please upload documents.",
            "source_documents": []
        }

    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})

    # ✅ Create chain fresh each time (lightweight)
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True
    )

    try:
        result = qa_chain({
            "question": query,
            "chat_history": chat_history
        })
        save_chat_history(query, result["answer"])
        return result
    except Exception as e:
        return {
            "answer": f"❌ Error while generating response: {str(e)}",
            "source_documents": []
        }
