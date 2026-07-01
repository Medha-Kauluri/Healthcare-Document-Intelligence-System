def confidence_score(
    verification,
    consensus
):

    score = 0

    if "SUPPORTED" in verification:
        score += 50

    score += consensus // 2

    return score