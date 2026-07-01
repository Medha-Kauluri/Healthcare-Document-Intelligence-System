# agents/risk_agent.py

def risk_analysis(
    llm,
    context
):

    prompt = f"""
Analyze the document.

Identify:

- Potential health risks
- Severity level
- Supporting evidence

Context:
{context}
"""

    response = llm.invoke(prompt)

    return response.content