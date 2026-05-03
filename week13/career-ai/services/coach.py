from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from app.config import GROQ_API_KEY
from services.vector_store import retrieve_context, load_vectorstore

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=GROQ_API_KEY
)

def generate_answer(user_id: str, question: str):
    # Check if vector store exists at all
    if load_vectorstore() is None:
        return "⚠️ Please upload a resume first."

    context = retrieve_context(user_id, question)

    # If context is empty, LLM should still get the prompt but it will likely say "Not found"
    # Or we can provide a default empty string context
    if not context:
        context = "No relevant information found for this specific question."

    prompt = ChatPromptTemplate.from_template("""
You are a strict AI Career Coach.

Rules:
- Answer ONLY using the resume
- If information is not present → say "Not found in resume"
- Do NOT assume anything
- Keep answers clear and professional

Resume:
{context}

Question:
{question}
""")

    chain = prompt | llm

    response = chain.invoke({
        "context": context,
        "question": question
    })

    return response.content
