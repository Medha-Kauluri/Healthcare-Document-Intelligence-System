# agents/treatment_agent.py

def treatment_summary(
    llm,
    context
):

    prompt = f"""
Extract treatment information.

Provide:

- Medications
- Procedures
- Lifestyle recommendations

Context:
{context}
"""

    response = llm.invoke(prompt)

    return response.content