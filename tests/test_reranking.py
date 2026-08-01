from app.retrieval.retriever import search_document
from app.rag.reranker import rerank_documents


questions = [
    "How much stipend is provided to interns?",
    "Who is eligible for the internship?",
    "How many paid leaves do interns receive?",
    "Is accommodation provided to interns?",
]


for question in questions:

    print("\n")
    print("=" * 100)
    print("QUESTION:", question)
    print("=" * 100)

    candidates = search_document(
        query=question,
        document_id="test_001",
        k=10,
    )

    reranked = rerank_documents(
        question=question,
        results=candidates,
        min_relevance=0.65,
        top_n=5,
    )

    if not reranked:
        print("\nNO RELEVANT EVIDENCE")
        continue

    for rank, result in enumerate(
        reranked,
        start=1,
    ):

        doc = result.document

        print(
            f"\n#{rank}"
            f" | Vector: {result.vector_score:.4f}"
            f" | Relevance: {result.relevance_score:.4f}"
        )

        print(
            "Chunk:",
            doc.metadata.get("chunk_id")
        )

        print(
            "Reason:",
            result.reason
        )

        print(
            "\n",
            doc.page_content[:500]
        )