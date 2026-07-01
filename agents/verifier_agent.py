def verify_answer(
    llm,
    context,
    answer
):

    prompt = f"""
You are a fact checker.

Context:
{context}

Answer:
{answer}

Determine whether the answer
is fully supported.

Return only:

SUPPORTED

or

HALLUCINATION
"""

    result = llm.invoke(prompt)

    return result.content