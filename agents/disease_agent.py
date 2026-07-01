# agents/disease_agent.py

def explain_disease(
    llm,
    context
):

    prompt = f"""
You must answer ONLY using information
contained in the provided context.

If information is not present,
reply:

'Not found in the document.'

Do not use outside medical knowledge.

Context:

{context}
"""

    response = llm.invoke(prompt)

    return response.content