from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY

def ask_llm(context, query):
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.1,
        api_key=GROQ_API_KEY
    )
    
    prompt = f"""
You are an Enterprise AI Assistant.
Use the provided context to answer the question accurately.
If the answer is not in the context, say "Not found in documents".

Context:
{context}

Question:
{query}

Answer:
"""
    response = llm.invoke(prompt)
    return response.content
