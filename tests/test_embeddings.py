from app.model import embeddings


texts = [
    "Scholarship eligibility for engineering students",
    "Faculty recruitment rules"
]

vectors = embeddings.embed_documents(texts)

print("Number of vectors:", len(vectors))
print("Dimension:", len(vectors[0]))
print("First 5 values:", vectors[0][:5])