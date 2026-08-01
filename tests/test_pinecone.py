from app.ingestion.pdf_loader import load_pdf

from app.ingestion.metadata import (
    extract_metadata,
    attach_metadata,
)

from app.ingestion.chunker import chunk_documents

from app.retrieval.vector_store import (
    create_index,
    store_chunks,
)


# OCR
documents = load_pdf(
    file_path="data/uploads/sample_gr.pdf",
    document_id="test_001",
)

# Metadata
metadata = extract_metadata(documents)

documents = attach_metadata(
    documents,
    metadata,
)

# Chunking
chunks = chunk_documents(documents)

print("Total chunks:", len(chunks))

# Pinecone
create_index()

store_chunks(chunks)