import os
from dotenv import load_dotenv

load_dotenv()

MISTRAL_CHAT_MODEL = os.getenv(
    "MISTRAL_CHAT_MODEL",
    "mistral-small-latest"
)

MISTRAL_EMBED_MODEL = os.getenv(
    "MISTRAL_EMBED_MODEL",
    "mistral-embed"
)

MISTRAL_OCR_MODEL = os.getenv(
    "MISTRAL_OCR_MODEL",
    "mistral-ocr-latest",
)

PINECONE_INDEX_NAME = os.getenv(
    "PINECONE_INDEX_NAME",
    "maha-gr"
)
SUPABASE_URL = os.getenv("SUPABASE_URL")

SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")


