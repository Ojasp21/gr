from langchain_mistralai import ChatMistralAI , MistralAIEmbeddings
from app.config import (

    MISTRAL_CHAT_MODEL,

    MISTRAL_EMBED_MODEL,

    PINECONE_INDEX_NAME,

)


llm = ChatMistralAI(
    model=MISTRAL_CHAT_MODEL,
    temperature=0
)


embeddings = MistralAIEmbeddings(

    model=MISTRAL_EMBED_MODEL

)