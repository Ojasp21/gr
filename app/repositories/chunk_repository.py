from app.db.supabase import supabase


def insert_chunk(chunk):

    response = (
        supabase
        .table("chunks")
        .insert(chunk)
        .execute()
    )

    return response.data


def get_document_chunks(
    document_id: str,
):

    response = (
        supabase
        .table("chunks")
        .select("*")
        .eq("document_id", document_id)
        .execute()
    )

    return response.data

def delete_document_chunks(

    document_id: str,

):

    response = (

        supabase

        .table("chunks")

        .delete()

        .eq(

            "document_id",

            document_id,

        )

        .execute()

    )

    return response.data