from app.rag.rag import ask_document


question = "How many paid leaves do interns receive?"

result = ask_document(
    question=question,
    document_id="test_001",
)


print("\nQUESTION")
print("=" * 80)
print(question)


print("\nANSWER")
print("=" * 80)
print(result["answer"])


print("\nSOURCES")
print("=" * 80)

for source in result["sources"]:
    print(source)