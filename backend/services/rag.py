import os
import cohere
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.llms.base import LLM
from typing import Optional, List
from pydantic import Extra
from services.embedding_service import load_vectorstore
from services.chatmem import save_chat_history
from config import config

# 🔹 Setup Cohere client
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# 🔹 Custom Cohere LLM wrapper
class CohereLLM(LLM):
    model: str = config.CHAT_MODEL or "command"
    temperature: float = 0.3
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


# 🔹 Setup memory (in-memory buffer for conversational context)
memory = ConversationBufferMemory(
    return_messages=True,
    input_key="question",
    output_key="answer"
)

# 🔹 Main RAG interface
def answer_query(query, chat_history=[]):
    vectorstore = load_vectorstore()

    if not vectorstore:
        return {
            "answer": "⚠️ Retrieval not available. Please upload documents.",
            "source_documents": []
        }

    try:
        retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )

        llm = CohereLLM()

        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=memory,
            return_source_documents=True
        )

        result = qa_chain({
            "question": query,
            "chat_history": chat_history
        })

        # 💾 Save interaction to memory log
        save_chat_history(query, result["answer"])

        return result

    except Exception as e:
        print("❌ Error in answer_query:", e)
        return {
            "answer": f"❌ Error while generating response: {str(e)}",
            "source_documents": []
        }
