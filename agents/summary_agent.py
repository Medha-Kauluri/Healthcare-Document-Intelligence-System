def summarize_document(
    llm,
    context
):

    prompt = f"""
You are a healthcare document analyst.

Analyze the document and provide:

1. Objective
2. Dataset Information
3. Methodology
4. Model Architecture
5. Performance Metrics
6. Key Challenges
7. Future Enhancements

If information exists in the document,
extract the exact values.

Do not say "not specified"
unless it truly does not exist.

Context:

{context}
"""

    response = llm.invoke(prompt)

    return response.content