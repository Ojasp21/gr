from langchain_core.documents import Document

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

MIN_CHUNK_SIZE = 100
HEADERS_TO_SPLIT_ON = [
    ("#", "heading_1"),
    ("##", "heading_2"),
    ("###", "heading_3"),
    ("####", "heading_4"),
]


markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=HEADERS_TO_SPLIT_ON,
    strip_headers=False,
)


recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=200,
    separators=[
        "\n\n",
        "\n",
        ". ",
        "। ",
        " ",
        "",
    ],
)


def get_section(metadata: dict) -> str | None:

    for heading in [
        "heading_4",
        "heading_3",
        "heading_2",
        "heading_1",
    ]:
        value = metadata.get(heading)
        if value:
            return value

    return "General"


def split_page(
    page_document: Document,
) -> list[Document]:

    markdown_sections = markdown_splitter.split_text(
        page_document.page_content
    )

    chunks = []

    for section in markdown_sections:

        section_metadata = {
            **page_document.metadata,
            **section.metadata,
        }

        section_document = Document(
            page_content=section.page_content,
            metadata=section_metadata,
        )

        smaller_chunks = recursive_splitter.split_documents(
            [section_document]
        )

        for chunk in smaller_chunks:
            if len(chunk.page_content.strip()) >= MIN_CHUNK_SIZE:
                chunks.append(chunk)

    return chunks


def add_chunk_metadata(
    chunks: list[Document],
) -> list[Document]:

    for index, chunk in enumerate(chunks):

        document_id = chunk.metadata.get(
            "document_id",
            "unknown",
        )

        page = chunk.metadata.get(
            "page",
            0,
        )

        chunk.metadata["chunk_index"] = index

        chunk.metadata["chunk_id"] = (
            f"{document_id}_p{page}_c{index}"
        )

        section = get_section(chunk.metadata)

        if section:
            chunk.metadata["section"] = section

    return chunks


def chunk_documents(
    documents: list[Document],
) -> list[Document]:

    all_chunks = []

    for page_document in documents:

        page_chunks = split_page(page_document)

        document_id = page_document.metadata.get(
            "document_id",
            "unknown",
        )

        page = page_document.metadata.get(
            "page",
            0,
        )

        for index, chunk in enumerate(page_chunks):

            chunk.metadata["chunk_index"] = index

            chunk.metadata["chunk_id"] = (
                f"{document_id}_p{page}_c{index}"
            )

            section = get_section(chunk.metadata)

            if section:
                chunk.metadata["section"] = section

            all_chunks.append(chunk)

    return all_chunks