from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from app.model import llm
from enum import Enum


class DocumentCategory(str, Enum):

    SCHOLARSHIP = "Scholarship"
    ADMISSIONS = "Admissions"
    FEES = "Fees"
    EXAMINATION = "Examination"

    FACULTY = "Faculty"
    RECRUITMENT = "Recruitment"

    UNIVERSITY_ADMINISTRATION = "University Administration"

    INFRASTRUCTURE = "Infrastructure"

    RESEARCH = "Research"

    BUDGET = "Budget"

    RESERVATION = "Reservation"

    STUDENT_WELFARE = "Student Welfare"

    HOSTEL = "Hostel"

    CURRICULUM = "Curriculum"

    INTERNSHIP = "Internship"

    OTHER = "Other"


class DocumentType(str, Enum):
    
    GOVERNMENT_RESOLUTION = "Government Resolution"

    CIRCULAR = "Circular"

    NOTIFICATION = "Notification"

    ORDER = "Order"

    LETTER = "Letter"

    MEMORANDUM = "Memorandum"

    OTHER = "Other"

class DocumentLanguage(str, Enum):
    
    ENGLISH = "English"

    MARATHI = "Marathi"

    HINDI = "Hindi"

    MIXED = "Mixed"

    OTHER = "Other"

class GRMetadata(BaseModel):

    document_type: DocumentType = Field(
        description=(
            "Type of government document, such as Government Resolution, "
            "Circular, Notification, Letter, Order, Memorandum, or Other."
        )
    )

    gr_number: Optional[str] = Field(
        default=None,
        description=(
            "Government Resolution number exactly as written in the document. "
            "Return null if this is not a Government Resolution or no GR number exists."
        )
    )

    department: Optional[str] = Field(
        default=None,
        description="Government department or organization issuing the document."
    )

    subject: Optional[str] = Field(
        default=None,
        description="Subject or main title of the document."
    )

    date: Optional[str] = Field(
        default=None,
        description="Document issue date exactly as written in the document."
    )

    language: DocumentLanguage = Field(
        description=(
            "Primary language of the document. "
            "Use English, Marathi, Hindi, or Mixed."
        )
    )

    category: DocumentCategory = Field(
        description=(
            "Main policy category of the document, such as Scholarship, "
            "Admissions, Fees, Examination, Faculty, Recruitment, "
            "University Administration, Infrastructure, Research, "
            "Budget, Reservation, Student Welfare, Hostel, Curriculum, "
            "Internship, or Other."
        )
    )

    subcategory: Optional[str] = Field(
        default=None,
        description="More specific category if clearly identifiable."
    )

    referenced_grs: list[str] = Field(
        default_factory=list,
        description=(
            "GR numbers explicitly referenced by this document. "
            "Do not invent GR numbers."
        )
    )
    



metadata_llm = llm.with_structured_output(GRMetadata)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You extract metadata from official Government of Maharashtra documents.

The documents may be written in:
- English
- Marathi
- Hindi
- or a mixture of these languages.

Extract metadata only from information supported by the provided document.

Rules:

1. Never invent a Government Resolution number.
2. Never invent dates.
3. Preserve GR numbers exactly as written.
4. Preserve the subject meaning accurately.
5. Identify the issuing department or organization.
6. Classify the document based on its actual subject.
7. If information is unavailable, return null where allowed.
8. referenced_grs must contain only GR numbers explicitly mentioned
   in the document.
9. Do not treat unrelated numbers, phone numbers, dates, file numbers,
   or monetary values as GR numbers.
10. The document may not actually be a Government Resolution.
    Correctly identify letters, circulars, notifications, orders, etc.
"""
        ),
        (
            "human",
            """
Extract metadata from the following government document:

{document}
"""
        ),
    ]
)


metadata_chain = prompt | metadata_llm


def extract_metadata(documents) -> GRMetadata:
    
    if not documents:
        raise ValueError("No documents provided.")

    text = "\n\n".join(
        doc.page_content
        for doc in documents
    )

    metadata = metadata_chain.invoke(
        {
            "document": text
        }
    )

    return metadata

def attach_metadata(
    documents,
    metadata: GRMetadata,
):

    extracted = metadata.model_dump(
        mode="json"
    )

    for document in documents:

        document.metadata.update(
            {
                key: value
                for key, value in extracted.items()
                if value is not None
            }
        )

    return documents