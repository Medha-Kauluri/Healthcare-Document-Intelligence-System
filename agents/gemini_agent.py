import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def gemini_answer(
    context,
    query
):

    prompt = f"""
Answer ONLY using the context.

Context:
{context}

Question:
{query}
"""

    response = model.generate_content(
        prompt
    )

    return response.text