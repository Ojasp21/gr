import requests
 
BASE_URL = "http://127.0.0.1:8000"
 
 
# ----------------------------------------
# Upload
# ----------------------------------------
 
def upload_document(uploaded_file):
 
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            "application/pdf",
        )
    }
 
    response = requests.post(
        f"{BASE_URL}/documents/upload",
        files=files,
    )
 
    response.raise_for_status()
 
    return response.json()
 
 
# ----------------------------------------
# Documents
# ----------------------------------------
 
def get_documents():
 
    response = requests.get(
        f"{BASE_URL}/documents"
    )
 
    response.raise_for_status()
 
    return response.json()
 
 
# ----------------------------------------
# Delete
# ----------------------------------------
 
def delete_document(
    document_id,
):
 
    response = requests.delete(
        f"{BASE_URL}/documents/{document_id}"
    )
 
    response.raise_for_status()
 
    return response.json()
 
 
# ----------------------------------------
# Global Chat
# ----------------------------------------
 
def ask_global(
    question,
):
 
    response = requests.post(
        f"{BASE_URL}/chat/global",
        json={
            "question": question,
        },
    )
 
    response.raise_for_status()
 
    return response.json()
 
 
# ----------------------------------------
# Document Chat
# ----------------------------------------
 
def ask_document(
    question,
    document_id,
):
 
    response = requests.post(
        f"{BASE_URL}/chat/document",
        json={
            "question": question,
            "document_id": document_id,
        },
    )
 
    response.raise_for_status()
 
    return response.json()
 
 
# ----------------------------------------
# Category Chat
# ----------------------------------------
 
def ask_category(
    question,
    category,
):
 
    response = requests.post(
        f"{BASE_URL}/chat/category",
        json={
            "question": question,
            "category": category,
        },
    )
 
    response.raise_for_status()
 
    return response.json()