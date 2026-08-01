from fastapi import APIRouter

from app.api.schemas import (
    ChatResponse,
    DocumentQuestionRequest,
    GlobalQuestionRequest,
    CategoryQuestionRequest,
)

from app.rag.rag import (
    ask_document,
    ask_global,
    ask_category,
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "/document",
    response_model=ChatResponse,
)
def chat_with_document(
    request: DocumentQuestionRequest,
):

    result = ask_document(
        question=request.question,
        document_id=request.document_id,
    )

    return result

@router.post(
    "/global",
    response_model=ChatResponse,
)
def global_chat(
    request: GlobalQuestionRequest,
):

    result = ask_global(
        question=request.question,
    )

    return result

@router.post(
    "/category",
    response_model=ChatResponse,
)
def chat_with_category(
    request: CategoryQuestionRequest,
):

    result = ask_category(
        question=request.question,
        category=request.category,
    )

    return result