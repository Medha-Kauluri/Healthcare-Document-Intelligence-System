def patient_explanation(llm, context):

    prompt = f"""
You are a healthcare assistant.

Explain this medical report in simple language.

For each test:

1. Test name
2. Result
3. Whether it is normal or abnormal
4. What it means in simple language

Use only information present in the report.

At the end provide:

Overall Health Summary

Context:

{context}
"""
    
    response = llm.invoke(prompt)

    return response.content