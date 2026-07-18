"""
Sentiment Analysis Module
---------------------------
Uses VADER (Valence Aware Dictionary and sEntiment Reasoner) to gauge the
emotional tone of a user's message.

WHY VADER: it's tuned for informal/conversational text (chat messages,
social media) rather than formal writing - a good fit for a chatbot.
It's fast (no model download/training needed) and gives interpretable
scores, which is useful when you need to explain your choices in a
resume/interview context.
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text: str) -> dict:
    """
    Returns sentiment scores for the given text.

    VADER gives:
      - neg, neu, pos: proportions of negative/neutral/positive content
      - compound: a single score from -1 (most negative) to +1 (most positive)

    We also bucket the compound score into a simple label for easier use
    in response logic.
    """
    if not text or not text.strip():
        return {"compound": 0.0, "label": "neutral", "scores": {"neg": 0, "neu": 1, "pos": 0}}

    scores = _analyzer.polarity_scores(text)
    compound = scores["compound"]

    if compound <= -0.5:
        label = "very_negative"
    elif compound <= -0.1:
        label = "negative"
    elif compound < 0.1:
        label = "neutral"
    elif compound < 0.5:
        label = "positive"
    else:
        label = "very_positive"

    return {
        "compound": compound,
        "label": label,
        "scores": {"neg": scores["neg"], "neu": scores["neu"], "pos": scores["pos"]},
    }