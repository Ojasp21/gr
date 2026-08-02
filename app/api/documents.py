import shutil
import uuid
from pathlib import Path
import traceback

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.ingestion.pdf_loader import load_pdf
from app.ingestion.metadata import (
    extract_metadata,
    attach_metadata,
)
from app.ingestion.chunker import chunk_documents
from app.retrieval.vector_store import store_chunks

from app.storage.storage import upload_pdf
from app.repositories.document_repository import (
    create_document,
    update_document,
)
from app.repositories.chunk_repository import insert_chunk

from app.repositories.document_repository import (

    get_document,

    delete_document,

)

from app.repositories.chunk_repository import (

    get_document_chunks,

    delete_document_chunks,

)

from app.retrieval.vector_store import (

    delete_chunks,

)

from app.storage.storage import (

    delete_pdf,

)
from app.repositories.document_repository import (

    get_all_documents,

)

from app.storage.storage import (

    get_document_url,

)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
):
    # --------------------------------
    # Validate file
    # --------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    # --------------------------------
    # Temporary file
    # --------------------------------

    temp_id = str(uuid.uuid4())
    safe_filename = Path(file.filename).name

    file_path = (
        UPLOAD_DIR
        / f"{temp_id}_{safe_filename}"
    )

    document_id = None

    try:

        # --------------------------------
        # Save uploaded PDF temporarily
        # --------------------------------

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        # --------------------------------
        # Upload PDF to Supabase Storage
        # --------------------------------

        storage_path = upload_pdf(
            str(file_path)
        )

        if not storage_path:
            raise ValueError(
                "Failed to upload PDF to Supabase Storage."
            )

        # --------------------------------
        # Create document record
        # --------------------------------

        document = create_document(
            {
                "filename": storage_path,
                "original_filename": safe_filename,
                "storage_path": storage_path,
                "status": "PROCESSING",
            }
        )

        document_id = document["id"]

        # --------------------------------
        # OCR
        # --------------------------------

        documents = load_pdf(
            file_path=str(file_path),
            document_id=document_id,
        )
        for document in documents:
            document.metadata["storage_path"] = storage_path
            document.metadata["original_filename"] = safe_filename
            
            
        if not documents:
            raise ValueError(
                "No text could be extracted from the PDF."
            )

        # --------------------------------
        # Metadata Extraction
        # --------------------------------

        metadata = extract_metadata(
            documents
        )

        documents = attach_metadata(
            documents,
            metadata,
        )

        # --------------------------------
        # Chunking
        # --------------------------------

        chunks = chunk_documents(
            documents
        )

        if not chunks:
            raise ValueError(
                "No usable chunks were generated."
            )

        # --------------------------------
        # Store in Pinecone
        # --------------------------------

        store_chunks(chunks)
        print("\n========== CHUNK METADATA ==========")

        for chunk in chunks:

            print(chunk.metadata)

        print("====================================")
        for chunk in chunks:
            insert_chunk(
         {
            "chunk_id": chunk.metadata["chunk_id"],
            "document_id": document_id,
            "page": chunk.metadata["page"],
            "section": chunk.metadata["section"],
            "pinecone_id": chunk.metadata["chunk_id"],
         }
      )

        # --------------------------------
        # Update document metadata
        # --------------------------------

        update_document(
            document_id,
            {
                "status": "READY",
                "category": metadata.category,
                "department": metadata.department,
                "language": metadata.language,
                "document_type": metadata.document_type,
                "subject": metadata.subject,
                "gr_number": metadata.gr_number,
                "pages": len(documents),
                "chunk_count": len(chunks),
            },
        )

        # --------------------------------
        # Success Response
        # --------------------------------

        return {
            "document_id": document_id,
            "status": "READY",
            "filename": safe_filename,
            "storage_path": storage_path,
            "pages": len(documents),
            "chunks": len(chunks),
            "metadata": metadata.model_dump(
                mode="json"
            ),
        }
    
    except Exception as exc:

    # Print the complete traceback

        traceback.print_exc()

        print("\n========== ERROR ==========")

        print(type(exc))

        print(exc)

        print("===========================\n")

        # Mark document as FAILED

        if document_id is not None:

            try:

                update_document(

                    document_id,

                    {

                        "status": "FAILED",

                    },

                )

            except Exception:

                traceback.print_exc()

        raise HTTPException(

            status_code=500,

            detail=str(exc),

        ) from exc

    finally:

        file.file.close()

        # Delete temporary local file

        if file_path.exists():
            file_path.unlink()
            
            
@router.delete("/{document_id}")
def delete_uploaded_document(
    document_id: str,
):

    document = get_document(
        document_id
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    chunks = get_document_chunks(
        document_id
    )

    chunk_ids = [
        chunk["chunk_id"]
        for chunk in chunks
    ]

    # Delete vectors

    delete_chunks(
        chunk_ids
    )

    # Delete PDF

    delete_pdf(
        document["storage_path"]
    )

    # Delete chunk rows

    delete_document_chunks(
        document_id
    )

    # Delete document row

    delete_document(
        document_id
    )

    return {
        "message":
            "Document deleted successfully.",
        "document_id":
            document_id,
    }
    
@router.get("")
def list_documents():

    documents = get_all_documents()

    for document in documents:

        document["view_url"] = get_document_url(
            document["storage_path"]
        )

    return documents