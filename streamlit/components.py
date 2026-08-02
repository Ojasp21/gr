import streamlit as st

# ----------------------------------------------------
# Status Badge
# ----------------------------------------------------

STATUS_STYLE = {
    "READY": ("badge-success", "Ready"),
    "PROCESSING": ("badge-warning", "Processing"),
    "FAILED": ("badge-danger", "Failed"),
}


def status_badge(status):

    css_class, label = STATUS_STYLE.get(
        status,
        ("badge-info", status),
    )

    return f"""<span class="badge {css_class}"><span class="badge-dot"></span>{label}</span>"""


# ----------------------------------------------------
# Source Card
# ----------------------------------------------------

def source_card(source):

    st.markdown(
        f"""
<div class="source-card">
    <div class="source-title">📄 {source.get('source', 'Unknown')}</div>
    <div class="source-meta">
        <span><b>Page</b> {source.get('page', '-')}</span>
        <span><b>Section</b> {source.get('section', '-')}</span>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    if source.get("view_url"):

        st.link_button(
            "📄  View Original PDF",
            source["view_url"],
            use_container_width=True,
        )


# ----------------------------------------------------
# Assistant Sources
# ----------------------------------------------------

def show_sources(sources):

    if not sources:
        return

    with st.expander(
        f"📚  Sources ({len(sources)})",
        expanded=False,
    ):

        for source in sources:

            source_card(source)


# ----------------------------------------------------
# User Message
# ----------------------------------------------------

def user_message(text):

    with st.chat_message("user"):

        st.markdown(text)


# ----------------------------------------------------
# Assistant Message
# ----------------------------------------------------

def assistant_message(answer, sources):

    with st.chat_message("assistant"):

        st.markdown(answer)

        show_sources(sources)


# ----------------------------------------------------
# Empty Chat State
# ----------------------------------------------------

def show_empty_chat_state(chat_mode):

    hints = {
        "Global": "Ask anything across every uploaded Government Resolution.",
        "Document-Specific": "Pick a document in the sidebar, then ask a focused question.",
        "Category": "Pick a category in the sidebar, then ask a focused question.",
    }

    st.markdown(
        f"""
<div class="empty-state">
    <div class="icon">💬</div>
    <div class="title">No messages yet</div>
    <div class="subtitle">{hints.get(chat_mode, "Start the conversation below.")}</div>
</div>
""",
        unsafe_allow_html=True,
    )


# ----------------------------------------------------
# Chat History
# ----------------------------------------------------

def show_chat_history(messages):

    for message in messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if (
                message["role"] == "assistant"
                and message.get("sources")
            ):

                show_sources(
                    message["sources"]
                )


# ----------------------------------------------------
# Document Card
# ----------------------------------------------------

def document_card(document):

    badge_html = status_badge(document["status"])

    st.markdown(
        f"""
<div class="doc-card">
    <div class="doc-title">📄&nbsp; {document["original_filename"]}</div>
    {badge_html}
    <div class="doc-meta-row">
        <span><b>Category</b> {document["category"]}</span>
        <span><b>Department</b> {document["department"]}</span>
        <span><b>Pages</b> {document["pages"]}</span>
        <span><b>Chunks</b> {document["chunk_count"]}</span>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )


# ----------------------------------------------------
# Uploaded Documents Panel
# ----------------------------------------------------

def show_documents(
    documents,
    delete_callback,
):

    st.markdown(
        """
<div class="section-heading"> Uploaded Documents</div>
""",
        unsafe_allow_html=True,
    )

    if not documents:

        st.markdown(
            """
<div class="empty-state">
    <div class="icon">📂</div>
    <div class="title">No documents uploaded yet</div>
    <div class="subtitle">Upload a PDF from the sidebar to get started.</div>
</div>
""",
            unsafe_allow_html=True,
        )

        return

    st.markdown(
        f"""<div class="section-subtext">{len(documents)} document{'s' if len(documents) != 1 else ''} on file</div>""",
        unsafe_allow_html=True,
    )

    columns = st.columns(2, gap="medium")

    for index, document in enumerate(documents):

        with columns[index % 2]:

            with st.container(border=True):

                document_card(document)

                left, right = st.columns(2)

                with left:

                    if document.get("view_url"):

                        st.link_button(
                            "  View",
                            document["view_url"],
                            use_container_width=True,
                        )

                with right:

                    if st.button(
                        "  Delete",
                        key=document["id"],
                        use_container_width=True,
                    ):

                        delete_callback(
                            document["id"]
                        )