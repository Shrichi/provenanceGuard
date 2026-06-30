import re
import math


def get_structural_score(text: str) -> float:
    """
    Computes a stylometric score estimating AI likelihood based on:
    - Sentence length uniformity (low variance = more AI-like)
    - Type-token ratio (low vocabulary diversity = more AI-like)
    - Formal punctuation density (more commas/semicolons = more AI-like)

    Returns a float between 0.0 (likely human) and 1.0 (likely AI).
    """
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    words = re.findall(r'\b\w+\b', text.lower())

    if len(sentences) < 2 or len(words) < 10:
        return 0.5  # not enough text to analyze reliably

    # 1. Sentence length uniformity via coefficient of variation
    #    Low CV = uniform lengths = AI-like → high score
    lengths = [len(s.split()) for s in sentences]
    mean_len = sum(lengths) / len(lengths)
    std_dev = math.sqrt(sum((l - mean_len) ** 2 for l in lengths) / len(lengths))
    cv = std_dev / mean_len if mean_len > 0 else 0
    uniformity_score = max(0.0, 1.0 - cv)

    # 2. Type-token ratio: unique_words / total_words
    #    Low TTR = less vocabulary diversity = AI-like → high score
    ttr = len(set(words)) / len(words)
    ttr_score = 1.0 - ttr

    # 3. Formal punctuation density (commas, semicolons, colons per word)
    #    AI writing uses more formal connective punctuation
    formal_punct = sum(1 for c in text if c in ',;:')
    punct_density = formal_punct / len(words)
    punct_score = min(1.0, punct_density / 0.3)

    structural_score = (uniformity_score + ttr_score + punct_score) / 3
    return round(max(0.0, min(1.0, structural_score)), 4)


if __name__ == "__main__":
    test_cases = [
        (
            "clearly AI",
            "Artificial intelligence represents a transformative paradigm shift in "
            "modern society. It is important to note that while the benefits of AI "
            "are numerous, it is equally essential to consider the ethical implications. "
            "Furthermore, stakeholders across various sectors must collaborate to ensure "
            "responsible deployment."
        ),
        (
            "clearly human",
            "ok so i finally tried that new ramen place downtown and honestly? "
            "underwhelming. the broth was fine but they put WAY too much sodium in it "
            "and i was thirsty for like three hours after. my friend got the spicy "
            "version and said it was better. probably won't go back unless someone drags me there."
        ),
        (
            "borderline formal human",
            "The relationship between monetary policy and asset price inflation has been "
            "extensively studied in the literature. Central banks face a fundamental tension "
            "between their mandate for price stability and the unintended consequences of "
            "prolonged low interest rates on equity and real estate valuations."
        ),
        (
            "borderline lightly edited AI",
            "I've been thinking a lot about remote work lately. There are genuine tradeoffs — "
            "flexibility and no commute on one side, isolation and blurred work-life boundaries "
            "on the other. Studies show productivity varies widely by individual and role type."
        ),
    ]

    for label, text in test_cases:
        score = get_structural_score(text)
        print(f"[{label}] structural_score = {score:.4f}")
