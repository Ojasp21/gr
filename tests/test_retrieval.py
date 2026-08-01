from app.retrieval.retriever import search_documents


queries = [
    "How much stipend is provided to interns?",
    "What is the maximum internship duration?",
    "Who is eligible for the internship?",
    "What documents should students submit?",
]


for query in queries:

    print("\n")
    print("=" * 100)
    print("QUERY:", query)
    print("=" * 100)

    results = search_documents(
        query=query,
        k=1,
    )

    for rank, (doc, score) in enumerate(results, start=1):

        print(
            f"\n#{rank} | "
            f"Score: {score:.4f} | "
            f"Chunk: {doc.metadata.get('chunk_id')} | "
            f"Page: {doc.metadata.get('page')}"
        )

        print(
            doc.page_content
            .replace("\n", " ")
        )