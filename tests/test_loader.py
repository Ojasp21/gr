from app.ingestion.pdf_loader import load_pdf


documents = load_pdf(
    file_path="data/uploads/sample_gr.pdf",
    document_id="test_gr_001",
)


print("\nNumber of pages:", len(documents))


for doc in documents:

    print("\n" + "=" * 60)

    print("Metadata:")
    print(doc.metadata)

    print("\nContent:")
    print(doc.page_content[:1000])