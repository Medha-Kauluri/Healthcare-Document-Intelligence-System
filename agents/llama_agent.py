def llama_answer(
    llm,
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

    response = llm.invoke(prompt)

    return response.content