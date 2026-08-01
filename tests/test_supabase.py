from app.repositories.document_repository import (
    create_document,
    list_documents,
)

from app.config import SUPABASE_URL, SUPABASE_SERVICE_KEY

print("URL:", SUPABASE_URL)
print("KEY PREFIX:", SUPABASE_SERVICE_KEY[:15])

doc = create_document(
    {
        "filename": "sample.pdf",
        "original_filename": "sample.pdf",
        "storage_path": "documents/sample.pdf",
        "status": "PROCESSING",
    }
)

print("Inserted:")
print(doc)

print()

print("All documents:")

docs = list_documents()

for d in docs:
    print(d)