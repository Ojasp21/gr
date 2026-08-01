import os
from pathlib import Path

from langchain_core.documents import Document
from mistralai.client import Mistral

from app.config import MISTRAL_OCR_MODEL


client = Mistral(
    api_key=os.environ["MISTRAL_API_KEY"]
)


def upload_pdf(file_path: str) -> str:
    """
    Upload a PDF to Mistral and return its file ID.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"PDF not found: {file_path}"
        )

    if path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported.")

    with open(path, "rb") as pdf_file:
        uploaded_file = client.files.upload(
            file={
                "file_name": path.name,
                "content": pdf_file,
            },
            purpose="ocr",
        )

    return uploaded_file.id

def get_signed_url(file_id: str) -> str:
    """
    Get a temporary URL for an uploaded Mistral file.
    """

    signed_url = client.files.get_signed_url(
        file_id=file_id
    )

    return signed_url.url


def run_ocr(file_url: str):
    """
    Run Mistral OCR on the PDF.
    """

    response = client.ocr.process(
        model=MISTRAL_OCR_MODEL,

        document={
            "type": "document_url",
            "document_url": file_url,
        },

        include_image_base64=False,
    )

    return response

def ocr_to_documents(
    ocr_response,
    file_name: str,
    document_id: str,
) -> list[Document]:

    documents = []

    for page in ocr_response.pages:

        markdown = page.markdown

        if not markdown.strip():
            continue

        document = Document(
            page_content=markdown,

            metadata={
                "document_id": document_id,
                "source": file_name,
                "page": page.index + 1,
            },
        )

        documents.append(document)

    return documents

def load_pdf(
    file_path: str,
    document_id: str,
) -> list[Document]:

    path = Path(file_path)

    print(f"Uploading: {path.name}")

    file_id = upload_pdf(file_path)

    print(f"Uploaded file ID: {file_id}")

    file_url = get_signed_url(file_id)

    print("Running OCR...")

    ocr_response = run_ocr(file_url)

    documents = ocr_to_documents(
        ocr_response=ocr_response,
        file_name=path.name,
        document_id=document_id,
    )

    print(
        f"OCR complete: {len(documents)} pages extracted."
    )

    return documents