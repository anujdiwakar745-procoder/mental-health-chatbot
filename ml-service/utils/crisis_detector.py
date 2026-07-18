"""
Crisis Detection Module
------------------------
Detects language that may indicate a mental health crisis (e.g. suicidal
ideation, self-harm intent) using keyword/phrase matching.

DESIGN NOTE: This is intentionally rule-based, not ML-based.
Crisis detection is too high-stakes to rely on a probabilistic model alone -
false negatives here have serious consequences. Keyword matching is:
  - Predictable and auditable (you can list exactly what triggers it)
  - Fast (no model inference needed)
  - Easy to extend as you learn about edge cases

In a production/clinical setting, this list should be reviewed and expanded
by mental health professionals. This is a starting point for a student/
portfolio project, not a clinically validated system.
"""

import re

HIGH_SEVERITY_PATTERNS = [
    r"\bkill myself\b",
    r"\bsuicid(e|al)\b",
    r"\bend my life\b",
    r"\bwant to die\b",
    r"\bdon'?t want to (live|be alive)\b",
    r"\bno reason to live\b",
    r"\bharm(ing)? myself\b",
    r"\bhurt(ing)? myself\b",
    r"\bself[\s-]?harm\b",
    r"\bcut(ting)? myself\b",
    r"\boverdose\b",
    r"\bbetter off dead\b",
    r"\bplan to die\b",
]

MODERATE_SEVERITY_PATTERNS = [
    r"\bhopeless\b",
    r"\bcan'?t (go on|take it anymore|cope)\b",
    r"\bworthless\b",
    r"\bno point\b",
    r"\bgive up\b",
    r"\btrapped\b",
    r"\bburden to (everyone|others|my family)\b",
]

_HIGH_RE = [re.compile(p, re.IGNORECASE) for p in HIGH_SEVERITY_PATTERNS]
_MODERATE_RE = [re.compile(p, re.IGNORECASE) for p in MODERATE_SEVERITY_PATTERNS]


def detect_crisis(text: str) -> dict:
    """
    Scans input text for crisis-indicating language.
    Returns is_crisis (bool), severity ("high"/"moderate"/"none"),
    and matched_patterns (for internal logging, never shown to the user).
    """
    if not text or not text.strip():
        return {"is_crisis": False, "severity": "none", "matched_patterns": []}

    matched = []

    for pattern in _HIGH_RE:
        if pattern.search(text):
            matched.append(pattern.pattern)

    if matched:
        return {"is_crisis": True, "severity": "high", "matched_patterns": matched}

    for pattern in _MODERATE_RE:
        if pattern.search(text):
            matched.append(pattern.pattern)

    if matched:
        return {"is_crisis": True, "severity": "moderate", "matched_patterns": matched}

    return {"is_crisis": False, "severity": "none", "matched_patterns": []}


# Replace/expand with resources relevant to your target country.
CRISIS_RESOURCES = {
    "high": {
        "message": (
            "It sounds like you're going through something really painful right now. "
            "You don't have to face this alone - please reach out to a crisis line, "
            "they're free, confidential, and available right now."
        ),
        "resources": [
            {"name": "988 Suicide & Crisis Lifeline (US)", "contact": "Call or text 988"},
            {"name": "Crisis Text Line", "contact": "Text HOME to 741741"},
            {"name": "iCall (India)", "contact": "+91 9152987821"},
            {"name": "International Association for Suicide Prevention",
             "contact": "https://www.iasp.info/resources/Crisis_Centres/"},
        ],
    },
    "moderate": {
        "message": (
            "It sounds like things feel really heavy right now. That's a lot to carry. "
            "Would it help to talk through what's going on, or would you like some "
            "grounding exercises to help in this moment?"
        ),
        "resources": [
            {"name": "988 Suicide & Crisis Lifeline (US)", "contact": "Call or text 988"},
            {"name": "iCall (India)", "contact": "+91 9152987821"},
        ],
    },
}