import streamlit as st

from api import (
    upload_document,
    ask_global,
    ask_document,
    ask_category,
    get_documents,
    delete_document,
)

from styles import load_css

from components import (
    show_chat_history,
    assistant_message,
    user_message,
    show_documents,
    show_empty_chat_state,
)

# ----------------------------------------------------
# Page
# ----------------------------------------------------

st.set_page_config(
    page_title="Maha-GR AI Assistant",
    page_icon="📄",
    layout="wide",
)

load_css()

# ----------------------------------------------------
# Session State
# ----------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------------------------------
# Load Documents
# ----------------------------------------------------

try:

    documents = get_documents()

except Exception as e:

    st.error(
        f"Cannot connect to backend.\n\n{e}"
    )

    st.stop()

# ----------------------------------------------------
# Build Document Map
# ----------------------------------------------------

document_map = {}

for doc in documents:

    document_map[
        doc["original_filename"]
    ] = doc["id"]

# ----------------------------------------------------
# Build Categories
# ----------------------------------------------------

categories = sorted(

    list(

        {

            doc["category"]

            for doc in documents

            if doc["category"]

        }

    )

)

ready_count = sum(
    1 for doc in documents if doc["status"] == "READY"
)

# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------

with st.sidebar:

    st.markdown(
        """
<div class="sidebar-brand">
    <div class="dot"></div>
    <span>Maha-GR AI</span>
</div>
""",
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        '<div class="sidebar-section-label">Upload</div>',
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(

        "Choose PDF",

        type=["pdf"],

        label_visibility="collapsed",

    )

    if uploaded_file:

        st.success(
            f"📎 {uploaded_file.name}"
        )

        if st.button(

            "⬆️  Upload Document",

            use_container_width=True,

            type="primary",

        ):

            with st.spinner(

                "Uploading..."

            ):

                try:

                    upload_document(

                        uploaded_file

                    )

                    st.success(

                        "Upload Successful"

                    )

                    st.rerun()

                except Exception as e:

                    st.error(str(e))

    st.divider()

    st.markdown(
        '<div class="sidebar-section-label">Chat Mode</div>',
        unsafe_allow_html=True,
    )

    chat_mode = st.radio(

        "Chat mode",

        [

            "Global",

            "Document-Specific",

            "Category",

        ],

        label_visibility="collapsed",

    )

    selected_document = None

    selected_category = None

    # ------------------------------------------

    if chat_mode == "Document-Specific":

        if document_map:

            name = st.selectbox(

                "Document",

                list(

                    document_map.keys()

                ),

            )

            selected_document = (

                document_map[name]

            )

        else:

            st.info(

                "No uploaded documents."

            )

    # ------------------------------------------

    elif chat_mode == "Category":

        if categories:

            selected_category = st.selectbox(

                "Category",

                categories,

            )

        else:

            st.info(

                "No categories available."

            )

    st.divider()

    if st.button(

        "🧹  Clear Chat",

        use_container_width=True,

    ):

        st.session_state.messages = []

        st.rerun()

# ----------------------------------------------------
# Main Header
# ----------------------------------------------------

st.markdown(
    """
<div class="app-header">
    <div class="icon-badge">🤖</div>
    <div>
        <h1>Government Resolution Assistant</h1>
        <p>Ask questions over uploaded Government Resolution documents.</p>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

stat_cols = st.columns(3)

stats = [
    ("Total Documents", len(documents)),
    ("Ready", ready_count),
    ("Active Mode", chat_mode),
]

for col, (label, value) in zip(stat_cols, stats):

    with col:

        st.markdown(
            f"""
<div class="stat-pill">
    <div class="stat-label">{label}</div>
    <div class="stat-value">{value}</div>
</div>
""",
            unsafe_allow_html=True,
        )

st.write("")

# ----------------------------------------------------
# Tabs
# ----------------------------------------------------

chat_tab, documents_tab = st.tabs(
    ["💬  Chat", "📂  Documents"]
)

# ----------------------------------------------------
# Chat Tab
# ----------------------------------------------------

with chat_tab:

    if st.session_state.messages:

        show_chat_history(
            st.session_state.messages
        )

    else:

        show_empty_chat_state(chat_mode)

    question = st.chat_input(
        "Ask a question..."
    )

    if question:

        # -----------------------------
        # Save User Message
        # -----------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        user_message(question)

        # -----------------------------
        # Backend Call
        # -----------------------------

        with st.spinner(
            "Searching documents..."
        ):

            try:

                if chat_mode == "Global":

                    result = ask_global(
                        question
                    )

                elif chat_mode == "Document-Specific":

                    if selected_document is None:

                        st.warning(
                            "Please select a document."
                        )

                        st.stop()

                    result = ask_document(
                        question=question,
                        document_id=selected_document,
                    )

                else:

                    if selected_category is None:

                        st.warning(
                            "Please select a category."
                        )

                        st.stop()

                    result = ask_category(
                        question=question,
                        category=selected_category,
                    )

            except Exception as e:

                st.error(str(e))
                st.stop()

        answer = result.get(
            "answer",
            "No answer returned."
        )

        sources = result.get(
            "sources",
            [],
        )

        assistant_message(
            answer,
            sources,
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": sources,
            }
        )

# ----------------------------------------------------
# Documents Tab
# ----------------------------------------------------

with documents_tab:

    def handle_delete(document_id):

        try:

            delete_document(
                document_id
            )

            st.success(
                "Document deleted successfully."
            )

            st.rerun()

        except Exception as e:

            st.error(str(e))


    show_documents(
        documents,
        handle_delete,
    )

# ----------------------------------------------------
# Footer
# ----------------------------------------------------

st.divider()

st.caption(
    """
Government of Maharashtra RAG Assistant

Powered by FastAPI • Pinecone • Supabase • LangChain • Mistral AI • Streamlit
"""
)