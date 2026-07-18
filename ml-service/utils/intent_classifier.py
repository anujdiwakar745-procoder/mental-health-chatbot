"""
Intent Classification Module
------------------------------
Identifies the general topic/category of a user's message (anxiety,
stress, sleep, loneliness, etc.) using keyword matching.

WHY RULE-BASED FOR NOW: Training a real ML classifier needs a labeled
dataset (thousands of example messages tagged by category), which takes
time to build or source. Keyword matching gets a working end-to-end demo
running fast. Swapping this for a fine-tuned model (e.g. DistilBERT) later
is a natural "v2" improvement to mention in your README as future work -
that's a legitimate, honest way to show growth in a portfolio project.
"""

import re

INTENT_PATTERNS = {
    "anxiety": [
        r"\banxious\b", r"\banxiety\b", r"\bpanic\b", r"\bnervous\b",
        r"\boverwhelm(ed|ing)?\b", r"\bworried\b", r"\bworry(ing)?\b",
        r"\bracing (thoughts|mind|heart)\b", r"\bon edge\b",
    ],
    "stress": [
        r"\bstress(ed|ful)?\b", r"\bburn(ed|t)? out\b", r"\btoo much\b",
        r"\bpressure\b", r"\bdeadline\b", r"\bexhaust(ed|ing)\b",
    ],
    "sadness": [
        r"\bsad\b", r"\bdown\b", r"\bdepress(ed|ing)?\b", r"\bcrying\b",
        r"\bcry(ing)?\b", r"\bempty\b", r"\bnumb\b", r"\bunhappy\b",
    ],
    "sleep": [
        r"\bcan'?t sleep\b", r"\binsomnia\b", r"\btired\b", r"\bexhausted\b",
        r"\bsleep(less|ing)?\b", r"\bawake all night\b", r"\bnightmares?\b",
    ],
    "loneliness": [
        r"\blonely\b", r"\balone\b", r"\bisolat(ed|ion)\b", r"\bno friends\b",
        r"\bno one (understands|cares)\b", r"\bdisconnected\b",
    ],
    "anger": [
        r"\bangry\b", r"\bfurious\b", r"\bfrustrat(ed|ing)\b", r"\birritat(ed|ing)\b",
        r"\bmad\b", r"\brage\b",
    ],
    "greeting": [
        r"^\s*hi\s*$", r"^\s*hello\s*$", r"^\s*hey\s*$", r"\bgood (morning|evening|afternoon)\b",
    ],
}

_COMPILED_PATTERNS = {
    intent: [re.compile(p, re.IGNORECASE) for p in patterns]
    for intent, patterns in INTENT_PATTERNS.items()
}


def classify_intent(text: str) -> dict:
    """
    Scans text against known intent categories.
    Returns the best-matching intent and a list of all matched intents
    (a message can touch multiple topics, e.g. stress + sleep).

    If nothing matches, returns intent="general" so the chatbot can fall
    back to an open-ended, empathetic response.
    """
    if not text or not text.strip():
        return {"intent": "general", "all_matches": []}

    matches = []
    for intent, patterns in _COMPILED_PATTERNS.items():
        for pattern in patterns:
            if pattern.search(text):
                matches.append(intent)
                break  # one match per intent category is enough

    if not matches:
        return {"intent": "general", "all_matches": []}

    # Simple priority order when multiple intents match -
    # emotional/safety-adjacent topics take precedence over greetings etc.
    priority = ["sadness", "anxiety", "loneliness", "anger", "stress", "sleep", "greeting"]
    best = next((i for i in priority if i in matches), matches[0])

    return {"intent": best, "all_matches": matches}