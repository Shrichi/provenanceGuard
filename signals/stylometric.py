import re
import math

# Transitional and hedging phrases that appear far more often in AI writing
# than in natural human prose
_AI_CONNECTIVES = [
    'furthermore', 'moreover', 'additionally', 'consequently', 'nevertheless',
    'therefore', 'in conclusion', 'in summary', 'to summarize', 'in addition',
    'it is important', 'it is worth', 'it should be noted', 'it is essential',
    'it is necessary', 'it is crucial', 'it is equally', 'it is therefore',
]


def get_structural_score(text: str) -> float | None:
    """
    Computes a stylometric score estimating AI likelihood based on five metrics:
    1. Sentence length uniformity (low variance = more AI-like)
    2. Type-token ratio (low vocabulary diversity = more AI-like)
    3. Formal punctuation density (more commas/semicolons = more AI-like)
    4. Average sentence length (longer sentences = more AI-like)
    5. AI connective phrase density (formulaic transitions = more AI-like)

    Returns a float between 0.0 (likely human) and 1.0 (likely AI),
    or None if the text is too short for reliable analysis.
    """
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    words = re.findall(r'\b\w+\b', text.lower())

    if len(sentences) < 2 or len(words) < 10:
        return None  # not enough text to analyze reliably

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

    # 4. Average sentence length
    #    AI tends to write longer, denser sentences (20+ words each)
    avg_len_score = min(1.0, mean_len / 20.0)

    # 5. AI connective/hedge phrase density
    #    Formulaic transitions are a strong AI marker
    text_lower = text.lower()
    hit_count = sum(1 for phrase in _AI_CONNECTIVES if phrase in text_lower)
    connective_score = min(1.0, hit_count / 3.0)  # 3+ distinct phrases = max score

    structural_score = (uniformity_score + ttr_score + punct_score + avg_len_score + connective_score) / 5
    return round(max(0.0, min(1.0, structural_score)), 4)


if __name__ == "__main__":
    test_cases = [
        (
            "clearly AI (long)",
            "Artificial intelligence is fundamentally reshaping the nature of work across virtually every sector of the global economy. Automation technologies, powered by increasingly sophisticated machine learning algorithms, are displacing routine cognitive tasks that were once the exclusive domain of human workers. It is important to acknowledge that while this transformation creates significant economic disruption, it also generates new categories of employment that require higher-order skills and creative problem-solving abilities.\n\nThe educational implications of this technological shift are profound and far-reaching. Traditional pedagogical models, which prioritized the transmission of factual knowledge and the development of standardized procedural skills, are becoming increasingly inadequate in preparing students for the demands of an AI-driven labor market. Educational institutions must therefore undergo substantial reform to emphasize critical thinking, adaptability, and the capacity for continuous learning.\n\nFurthermore, the distributional consequences of AI-driven automation are likely to exacerbate existing socioeconomic inequalities if left unaddressed by policy interventions. Policymakers must therefore develop targeted support mechanisms, including robust retraining programs and expanded social safety nets, to mitigate these adverse distributional effects. In conclusion, the responsible development of artificial intelligence requires a holistic approach that addresses economic, educational, and governance dimensions simultaneously."
        ),
        (
            "clearly human (long)",
            "i keep starting journals and abandoning them after like two weeks. not because i run out of things to say but because i reread what i wrote and it sounds nothing like how i actually think. written me is always somehow more composed and boring than real me, which is frustrating because the whole point was to capture something true.\n\nmaybe the problem is that writing forces you to finish your thoughts. when im just thinking i can trail off, backtrack, hold two contradictory things at once without resolving them. but the moment i write a sentence it has to go somewhere. it has to end. and the ending always feels like a lie because nothing in my head ever actually ends cleanly.\n\ntheres something almost embarrassing about how much i want to document my own life. like who do i think is going to read this. nobody. not even future me, probably, because future me will have moved on to new anxieties and wont care what current me was worried about."
        ),
    ]

    for label, text in test_cases:
        score = get_structural_score(text)
        print(f"[{label}] structural_score = {score}")
