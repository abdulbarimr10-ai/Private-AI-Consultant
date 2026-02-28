from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

# LLM
def get_llm():
    return Ollama(
        model="phi3:mini",
        request_timeout=120.0,
        additional_kwargs={
            "num_ctx": 2048   # 🔥 force small context window
        }
    )
# Embedding model
def get_embedding_model():
    print("Using embedding: nomic-embed-text")
    return OllamaEmbedding(
        model_name="nomic-embed-text"
    )

SYSTEM_PROMPT = """
You are a private consultant.

Only answer using the uploaded document.
If the answer is not in the document,
say: "I don't have that information in my knowledge base."

Do not use outside knowledge.
"""