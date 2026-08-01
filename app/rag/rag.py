from langchain_core.prompts import ChatPromptTemplate

from app.model import llm
from app.retrieval.retriever import (
    search_documents,
    search_document,
    search_category,
)
from app.rag.reranker import rerank_documents
from app.storage.storage import get_signed_url

rag_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an AI assistant for Government of Maharashtra documents.

Answer the user's question ONLY using the provided source context.

Rules:

1. Do not use outside knowledge.
2. Do not invent facts, dates, amounts, GR numbers, eligibility
   criteria, rules, policies, or other information.
3. Every factual claim must be supported by the provided sources.
4. If the sources do not contain enough information to answer the
   question, clearly state:
   "The provided documents do not contain sufficient information
   to answer this question."
5. If multiple sources contain conflicting information, explicitly
   mention the conflict instead of choosing one silently.
6. Preserve important numbers, dates, amounts, names and conditions
   exactly.
7. Answer in a clear and concise manner.
8. Cite sources using the source labels provided in the context,
   for example [Source 1].
9. Do not create source references that do not exist in the context.
"""
        ),
        (
            "human",
            """
Question:

{question}


Sources:

{context}


Answer the question using only the sources above.
"""
        ),
    ]
)

def format_context(results):
    
    context_parts = []

    for index, result in enumerate(
        results,
        start=1,
    ):

        doc = result.document

        source = doc.metadata.get(
            "source",
            "Unknown document",
        )

        page = doc.metadata.get(
            "page",
            "Unknown",
        )

        section = doc.metadata.get(
            "section",
        )

        gr_number = doc.metadata.get(
            "gr_number",
        )

        header = [
            f"[Source {index}]",
            f"Document: {source}",
            f"Page: {page}",
        ]

        if gr_number:
            header.append(
                f"GR Number: {gr_number}"
            )

        if section:
            header.append(
                f"Section: {section}"
            )

        context_parts.append(
            "\n".join(header)
            + "\n\n"
            + doc.page_content
        )

    return "\n\n---\n\n".join(
        context_parts
    )

def ask_global(
    question: str,
    candidate_k: int = 15,
    final_k: int = 5,
):

    candidates = search_documents(
        query=question,
        k=candidate_k,
    )

    if not candidates:
        return {
            "answer": (
                "The available documents do not contain "
                "sufficient information to answer this question."
            ),
            "sources": [],
        }

    relevant_documents = rerank_documents(
        question=question,
        results=candidates,
        min_relevance=0.65,
        top_n=final_k,
    )

    if not relevant_documents:
        return {
            "answer": (
                "The available documents do not contain "
                "sufficient information to answer this question."
            ),
            "sources": [],
        }

    context = format_context(
        relevant_documents
    )

    chain = rag_prompt | llm

    response = chain.invoke(
        {
            "question": question,
            "context": context,
        }
    )

    return {
        "answer": response.content,
        "sources": [
            build_source(result)
            for result in relevant_documents
        ],
    }
    
def build_source(result):
    
    metadata = result.document.metadata

    return {

        "document_id": metadata.get("document_id"),

        "document_name": metadata.get("original_filename"),

        "page": metadata.get("page"),

        "section": metadata.get("section"),

        "gr_number": metadata.get("gr_number"),

        "chunk_id": metadata.get("chunk_id"),

        "view_url": get_signed_url(

            metadata["storage_path"]

        ),

        "vector_score": result.vector_score,

        "relevance_score": result.relevance_score,

    }
    
    
NO_ANSWER = (
    "The selected document does not contain sufficient "
    "information to answer this question."
)


def ask_document(
    question: str,
    document_id: str,
    candidate_k: int = 15,
    final_k: int = 5,
):

    candidates = search_document(
        query=question,
        document_id=document_id,
        k=candidate_k,
    )

    if not candidates:
        return {
            "answer": NO_ANSWER,
            "sources": [],
        }

    relevant_documents = rerank_documents(
        question=question,
        results=candidates,
        min_relevance=0.65,
        top_n=final_k,
    )

    if not relevant_documents:
        return {
            "answer": NO_ANSWER,
            "sources": [],
        }

    context = format_context(
        relevant_documents
    )

    chain = rag_prompt | llm

    response = chain.invoke(
        {
            "question": question,
            "context": context,
        }
    )

    return {
        "answer": response.content,

        "sources": [
            build_source(result)
            for result in relevant_documents
        ],
    }
    
CATEGORY_NO_ANSWER = (
    "The documents in the selected category do not contain "
    "sufficient information to answer this question."
)
    
def ask_category(
    question: str,
    category: str,
    candidate_k: int = 15,
    final_k: int = 5,
):

    candidates = search_category(
        query=question,
        category=category,
        k=candidate_k,
    )

    if not candidates:
        return {
            "answer": (
                "No relevant information was found "
                "in this category."
            ),
            "sources": [],
        }
    
    relevant_documents = rerank_documents(
            question=question,
            results=candidates,
            min_relevance=0.65,
            top_n=final_k,
        )
    
    if not relevant_documents:
            return {
                "answer": CATEGORY_NO_ANSWER,
                "sources": [],
            }

    context = format_context(relevant_documents)

    chain = rag_prompt | llm

    response = chain.invoke(
        {
            "question": question,
            "context": context,
        }
    )

    return {
        "answer": response.content,
        "sources": [
            build_source(result)
            for result in relevant_documents
        ],
    }