# agents/retriever_agent.py

import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_community.vectorstores import Pinecone as LangchainPinecone
from langchain.text_splitter import CharacterTextSplitter

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
PINECONE_ENV = os.getenv("PINECONE_ENV", "gcp-starter")  # fallback if unset

pc = Pinecone(api_key=PINECONE_API_KEY)


def init_pinecone_index():
    if not pc.has_index(PINECONE_INDEX_NAME):
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=1024,  # Match your Pinecone index setting
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )


def build_pinecone_index(doc_texts):
    init_pinecone_index()
    splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    chunks = splitter.split_texts(doc_texts)

    if not chunks:
        print("[WARN] No chunks generated from input texts.")
        return False

    vectorstore = LangchainPinecone.from_existing_index(
        index_name=PINECONE_INDEX_NAME,
        embedding=None  # Pinecone-native model
    )

    print(f"[INFO] Inserting {len(chunks)} chunks into Pinecone index '{PINECONE_INDEX_NAME}'...")
    vectorstore.add_texts(chunks)
    print("[INFO] Chunks added to Pinecone successfully.")

    # Optional verification: count records in Pinecone index
    index = pc.Index(PINECONE_INDEX_NAME)
    stats = index.describe_index_stats()
    print(f"[DEBUG] Pinecone index record count: {stats.get('total_vector_count', 0)}")

    return True


def retrieve_chunks_from_pinecone(query, k=3):
    vectorstore = LangchainPinecone.from_existing_index(
        index_name=PINECONE_INDEX_NAME,
        embedding=None  # Must be None for Pinecone-native
    )
    return vectorstore.similarity_search(query, k=k)
