from pydantic import BaseModel, Field


class DocumentQuestionRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=2000,
    )

    document_id: str


class CategoryQuestionRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=2000,
    )

    category: str

class GlobalQuestionRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=2000,
    )


class SourceResponse(BaseModel):
    document_id: str | None = None
    source: str | None = None
    page: float | int | None = None
    section: str | None = None
    gr_number: str | None = None
    chunk_id: str | None = None
    view_url: str | None = None
    vector_score: float | None = None
    relevance_score: float | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]