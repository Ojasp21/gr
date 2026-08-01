from app.retrieval.vector_store import get_vector_store


def search_documents(
    query: str,
    k: int = 3,
):
    vector_store = get_vector_store()

    results = vector_store.similarity_search_with_score(
        query=query,
        k=k,
    )

    return results

def search_category(
    query: str,
    category: str,
    k: int = 5,
):
    vector_store = get_vector_store()

    return vector_store.similarity_search_with_score(
        query=query,
        k=k,
        filter={
            "category": category,
        },
    )
    
def search_document(
    query: str,
    document_id: str,
    k: int = 5,
):
    vector_store = get_vector_store()

    results = vector_store.similarity_search_with_score(
        query=query,
        k=k,
        filter={
            "document_id": document_id,
        },
    )

    return results