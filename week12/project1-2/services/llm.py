from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY

def ask_llm(query, context_texts):
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.1,
        api_key=GROQ_API_KEY
    )
    
    context = "\n\n".join(context_texts)
    
    prompt = f"""
Use the following context to answer the question.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{query}

Answer:
"""
    response = llm.invoke(prompt)
    return response.content
