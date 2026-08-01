from app.ingestion.pdf_loader import load_pdf
from app.ingestion.metadata import attach_metadata, extract_metadata


documents = load_pdf(
    file_path="data/uploads/sample_gr.pdf",
    document_id="test_001",
)


metadata = extract_metadata(documents)



documents = attach_metadata(
    documents,
    metadata,
)

print(documents[0].metadata)