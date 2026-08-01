from dataclasses import dataclass

from pydantic import BaseModel, Field
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from app.model import llm


# ============================================================
# Structured output schemas
# ============================================================

class CandidateRelevance(BaseModel):
    chunk_id: str = Field(
        description="The exact chunk ID provided in the candidate."
    )

    score: float = Field(
        ge=0.0,
        le=1.0,
        description=(
            "Relevance score between 0 and 1. "
            "This field is required for every candidate."
        ),
    )

    reason: str = Field(
        description=(
            "Short explanation of why the candidate "
            "is or is not relevant."
        )
    )


class RerankingResult(BaseModel):
    results: list[CandidateRelevance] = Field(
        description=(
            "Evaluation of every candidate provided. "
            "Every candidate must appear exactly once."
        )
    )


# ============================================================
# Internal representation after reranking
# ============================================================

@dataclass
class RerankedDocument:
    document: Document
    vector_score: float
    relevance_score: float
    reason: str


# ============================================================
# Structured Mistral model
# ============================================================

reranker_llm = llm.with_structured_output(
    RerankingResult
)


# ============================================================
# Prompt
# ============================================================

reranker_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a relevance evaluator for Government of Maharashtra documents.

You will receive:

1. A user question
2. Multiple candidate passages retrieved from a document database

Evaluate EVERY candidate independently.

Your job is NOT to answer the question.

Your job is to determine how useful each candidate passage is
for answering the user's question.

IMPORTANT:

- Return exactly one result for every candidate.
- Preserve each CHUNK_ID exactly as provided.
- score is REQUIRED for every candidate.
- reason is REQUIRED for every candidate.
- Never omit a candidate.
- Do not invent chunk IDs.
- Do not mark a passage highly relevant merely because it
  contains similar keywords.

Scoring:

0.90 - 1.00
The candidate directly contains the answer.

0.70 - 0.89
The candidate contains strong evidence useful for answering.

0.50 - 0.69
The candidate contains partial evidence.

0.20 - 0.49
The candidate discusses a related topic but does not provide
evidence answering the question.

0.00 - 0.19
The candidate is unrelated.

Only assign a high score when the passage contains actual
evidence useful for answering the question.
"""
        ),
        (
            "human",
            """
Question:

{question}


Candidates:

{candidates}
"""
        ),
    ]
)


reranker_chain = (
    reranker_prompt
    | reranker_llm
)


# ============================================================
# Candidate formatting
# ============================================================

def format_candidates(results) -> str:

    parts = []

    for document, _ in results:

        chunk_id = document.metadata.get(
            "chunk_id"
        )

        parts.append(
            f"""
CHUNK_ID: {chunk_id}

CONTENT:
{document.page_content}
"""
        )

    return "\n\n---\n\n".join(parts)


# ============================================================
# Batch reranking
# ============================================================

def rerank_documents(
    question: str,
    results,
    min_relevance: float = 0.65,
    top_n: int = 5,
) -> list[RerankedDocument]:

    if not results:
        return []

    # ----------------------------------
    # Prepare candidates
    # ----------------------------------

    candidates_text = format_candidates(
        results
    )

    # ----------------------------------
    # ONE Mistral call
    # ----------------------------------

    evaluation = reranker_chain.invoke(
        {
            "question": question,
            "candidates": candidates_text,
        }
    )

    # ----------------------------------
    # Map chunk IDs back to Documents
    # ----------------------------------

    candidate_map = {
        doc.metadata.get("chunk_id"): (
            doc,
            score,
        )
        for doc, score in results
    }

    # ----------------------------------
    # Check model returned every chunk
    # ----------------------------------

    expected_ids = set(
        candidate_map.keys()
    )

    returned_ids = {
        result.chunk_id
        for result in evaluation.results
    }

    missing_ids = (
        expected_ids - returned_ids
    )

    if missing_ids:
        print(
            "Warning: reranker did not evaluate:",
            missing_ids,
        )

    # ----------------------------------
    # Apply relevance threshold
    # ----------------------------------

    reranked = []

    for result in evaluation.results:

        if result.score < min_relevance:
            continue

        candidate = candidate_map.get(
            result.chunk_id
        )

        if candidate is None:
            continue

        document, vector_score = candidate

        reranked.append(
            RerankedDocument(
                document=document,
                vector_score=float(
                    vector_score
                ),
                relevance_score=result.score,
                reason=result.reason,
            )
        )

    # ----------------------------------
    # Highest relevance first
    # ----------------------------------

    reranked.sort(
        key=lambda item:
            item.relevance_score,
        reverse=True,
    )

    return reranked[:top_n]