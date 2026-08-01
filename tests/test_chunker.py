from app.ingestion.pdf_loader import load_pdf
from app.ingestion.metadata import (
    extract_metadata,
    attach_metadata,
)
from app.ingestion.chunker import chunk_documents


# 1. OCR
documents = load_pdf(
    file_path="data/uploads/sample_gr.pdf",
    document_id="test_001",
)


# 2. Extract metadata
metadata = extract_metadata(
    documents
)


# 3. Attach metadata
documents = attach_metadata(
    documents,
    metadata,
)


# 4. Chunk
chunks = chunk_documents(
    documents
)


print("\nTotal pages:", len(documents))
print("Total chunks:", len(chunks))


for chunk in chunks:

    print("\n" + "=" * 80)

    print("CHUNK ID:")
    print(chunk.metadata["chunk_id"])

    print("\nPAGE:")
    print(chunk.metadata["page"])

    print("\nSECTION:")
    print(
        chunk.metadata.get(
            "section",
            "No section detected"
        )
    )

    print("\nCATEGORY:")
    print(chunk.metadata.get("category"))

    print("\nCONTENT:")
    print(chunk.page_content)

    print("\nLENGTH:")
    print(len(chunk.page_content))