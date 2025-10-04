import json
import ollama
from src.embedder import cos_sim
from src.scraper import scrape_first_conversations
from src.chunks import chunk_text

def generate_answer(query, relevant_answers, temperature=0.1):
    """
    Generates a practical answer to a farmer's question using Ollama LLM.
    """
    # Build the context string from relevant answers
    context = "\n".join([f"{i+1}. {relevant_answers[i]}" for i in range(len(relevant_answers))])
    
    prompt = f"""
You are an agricultural assistant chatbot helping farmers. 
The farmer has asked the question: '{query}'.

You also have some background information from the internet:
{context}

Instructions:
- Your top priority is to give a direct, clear, and practical answer to the farmer’s question.
- If the background information is relevant, you may use it to enrich the answer.
- If it is not relevant, completely ignore it and focus only on the question.
- Do not summarize or retell the background story unless it helps the farmer with their specific question.
- Keep your answer simple, supportive, and easy for a farmer to apply in practice.
- Avoid names, places, or unnecessary storytelling from the background.
- Give practical advice or explanations the farmer can act on.

Final Answer for the farmer:
"""

    # Generate the response using Ollama chat API
    response = ollama.chat(
        model="llama3.2:3b",
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": temperature}  # set temperature here
    )

    # Extract the text from the response
    return str(response).strip()
