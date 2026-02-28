import os
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage
)


from llama_index.core.memory import ChatMemoryBuffer
from config import get_llm, get_embedding_model, SYSTEM_PROMPT
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.core.node_parser import SentenceSplitter



PERSIST_DIR = "storage"


def build_index_from_file(file_path):
    documents = SimpleDirectoryReader(
        input_files=[file_path]
    ).load_data()

    # 🔥 Reduce chunk size aggressively
    splitter = SentenceSplitter(
        chunk_size=512,        # small chunks
        chunk_overlap=50
    )

    nodes = splitter.get_nodes_from_documents(documents)

    index = VectorStoreIndex(
        nodes,
        embed_model=get_embedding_model()
    )

    index.storage_context.persist(persist_dir=PERSIST_DIR)

    return index


def load_existing_index():
    if not os.path.exists(PERSIST_DIR):
        return None

    storage_context = StorageContext.from_defaults(
        persist_dir=PERSIST_DIR
    )

    return load_index_from_storage(storage_context)


def get_query_engine(index):
    memory = ChatMemoryBuffer.from_defaults(
        token_limit=1500
    )

    return index.as_chat_engine(
        llm=get_llm(),
        memory=memory,
        similarity_top_k=2,
        system_prompt=SYSTEM_PROMPT,
        response_mode="simple_summarize"
    )