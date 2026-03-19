def score_headlines(headlines: list[str]) -> float:
    """
    Placeholder sentiment: +1 per bullish keyword, -1 per bearish.
    Later we can swap with a real model or API.
    """
    bull = {"beats", "surge", "rally", "up", "bull", "growth"}
    bear = {"miss", "plunge", "selloff", "down", "bear", "cut"}
    score = 0
    for h in headlines:
        lo = h.lower()
        score += sum(k in lo for k in bull)
        score -= sum(k in lo for k in bear)
    # squash to [-1,1]
    if score > 0: return min(1.0, 0.1 * score)
    if score < 0: return max(-1.0, 0.1 * score)
    return 0.0
