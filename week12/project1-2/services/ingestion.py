def load_documents_from_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]

    documents = []

    # Combine Q&A pairs safely (based on demo_app logic)
    for i in range(0, len(lines), 2):
        question = lines[i]
        answer = lines[i + 1] if i + 1 < len(lines) else ""
        documents.append(f"Q: {question}\nA: {answer}")

    return documents
