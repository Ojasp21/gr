from app.db.supabase import supabase


def get_document(
    document_id: str,
):

    response = (
        supabase
        .table("documents")
        .select("*")
        .eq(
            "id",
            document_id,
        )
        .single()
        .execute()
    )

    return response.data

def create_document(data):

    response = (
        supabase
        .table("documents")
        .insert(data)
        .execute()
    )

    return response.data[0]


def update_document(document_id, values):

    response = (
        supabase
        .table("documents")
        .update(values)
        .eq("id", document_id)
        .execute()
    )

    return response.data[0]


def delete_document(

    document_id: str,

):

    response = (

        supabase

        .table("documents")

        .delete()

        .eq(

            "id",

            document_id,

        )

        .execute()

    )

    return response.data