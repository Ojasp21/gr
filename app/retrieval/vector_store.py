import os

from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

from app.model import embeddings
from app.config import PINECONE_INDEX_NAME


pc = Pinecone(
    api_key=os.environ["PINECONE_API_KEY"]
)


def get_embedding_dimension() -> int:
    """
    Determine the vector dimension from the configured
    embedding model.
    """
    test_vector = embeddings.embed_query("dimension test")
    return len(test_vector)


def create_index():

    existing_indexes = [
        index.name
        for index in pc.list_indexes()
    ]

    if PINECONE_INDEX_NAME in existing_indexes:
        print(
            f"Index '{PINECONE_INDEX_NAME}' already exists."
        )
        return

    dimension = get_embedding_dimension()

    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=dimension,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1",
        ),
    )

    print(
        f"Created index '{PINECONE_INDEX_NAME}' "
        f"with dimension {dimension}."
    )


def get_vector_store():

    return PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,
        embedding=embeddings,
    )


def store_chunks(chunks):

    if not chunks:
        raise ValueError("No chunks provided.")

    vector_store = get_vector_store()

    ids = [
        chunk.metadata["chunk_id"]
        for chunk in chunks
    ]

    vector_store.add_documents(
        documents=chunks,
        ids=ids,
    )

    print(
        f"Stored {len(chunks)} chunks in Pinecone."
    )
    
    

def delete_chunks(chunk_ids: list[str]):
    
    if not chunk_ids:

        return

    index = pc.Index(PINECONE_INDEX_NAME)

    index.delete(

        ids=chunk_ids,

    )

    print(

        f"Deleted {len(chunk_ids)} vectors from Pinecone."

    )