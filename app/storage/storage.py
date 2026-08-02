import uuid
from pathlib import Path

from app.db.supabase import supabase
from app.config import SUPABASE_BUCKET


def upload_pdf(local_file: str) -> str:
    extension = Path(local_file).suffix

    storage_name = f"{uuid.uuid4()}{extension}"

    with open(local_file, "rb") as f:
        supabase.storage.from_(SUPABASE_BUCKET).upload(
            path=storage_name,
            file=f,
        )

    return storage_name



def get_signed_url(

    storage_path: str,

    expires_in: int = 3600,

) -> str:

    response = (

        supabase.storage

        .from_(SUPABASE_BUCKET)

        .create_signed_url(

            storage_path,

            expires_in,

        )

    )

    return response["signedURL"]


def delete_pdf(
    storage_path: str,

):

    (

        supabase.storage

        .from_(SUPABASE_BUCKET)

        .remove(

            [storage_path]

        )

    )
    


def get_document_url(
    storage_path: str,
):

    return (
        supabase.storage
        .from_(SUPABASE_BUCKET)
        .get_public_url(storage_path)
    )