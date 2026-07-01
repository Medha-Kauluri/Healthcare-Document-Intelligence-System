from difflib import SequenceMatcher

def consensus_score(
    llama_answer,
    gemini_answer
):

    similarity = SequenceMatcher(
        None,
        llama_answer.lower(),
        gemini_answer.lower()
    ).ratio()

    return int(
        similarity * 100
    )