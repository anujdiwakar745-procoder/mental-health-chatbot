"""
Response Generator Module
----------------------------
Maps detected intent + sentiment to evidence-based supportive responses:
CBT (Cognitive Behavioral Therapy) techniques, grounding exercises, and
mindfulness scripts.

SOURCING NOTE: These are simplified adaptations of well-established,
publicly documented techniques (e.g. 5-4-3-2-1 grounding, box breathing,
cognitive reframing from CBT). For your README, cite general sources like
NHS "Every Mind Matters," APA, or CDC mental health resources - and be
clear this is educational content, not a replacement for therapy.
"""

import random

RESPONSE_LIBRARY = {
    "anxiety": {
        "opener": [
            "It sounds like your mind is racing right now. Let's slow things down together.",
            "Anxiety can feel really overwhelming. You're not alone in this.",
        ],
        "technique": {
            "name": "5-4-3-2-1 Grounding Exercise",
            "description": (
                "This technique uses your senses to bring you back to the present moment:\n"
                "• Name 5 things you can SEE around you\n"
                "• Name 4 things you can TOUCH\n"
                "• Name 3 things you can HEAR\n"
                "• Name 2 things you can SMELL\n"
                "• Name 1 thing you can TASTE\n\n"
                "Take your time with each step. There's no rush."
            ),
        },
    },
    "stress": {
        "opener": [
            "That sounds like a lot to carry right now.",
            "Feeling stretched thin is exhausting. Let's take a moment to reset.",
        ],
        "technique": {
            "name": "Box Breathing",
            "description": (
                "This is used by professionals (even Navy SEALs) to calm the nervous system:\n"
                "• Breathe IN for 4 seconds\n"
                "• HOLD for 4 seconds\n"
                "• Breathe OUT for 4 seconds\n"
                "• HOLD for 4 seconds\n"
                "• Repeat 4 times\n\n"
                "Try it now if you can - even one round helps."
            ),
        },
    },
    "sadness": {
        "opener": [
            "I'm really sorry you're feeling this way. Your feelings are valid.",
            "That sounds really heavy. Thank you for sharing it with me.",
        ],
        "technique": {
            "name": "Cognitive Reframing (CBT)",
            "description": (
                "One CBT technique is noticing 'thinking traps' - patterns like "
                "all-or-nothing thinking or assuming the worst. Try asking yourself:\n"
                "• What's the evidence for and against this thought?\n"
                "• Would I say this to a friend in my situation?\n"
                "• Is there a more balanced way to see this?\n\n"
                "This isn't about forcing positivity - it's about finding a fairer view."
            ),
        },
    },
    "sleep": {
        "opener": [
            "Not being able to sleep is so draining, both mentally and physically.",
            "Sleep struggles are tough. Let's see if this helps tonight.",
        ],
        "technique": {
            "name": "Progressive Muscle Relaxation",
            "description": (
                "Lying down, work through your body from feet to head:\n"
                "• Tense each muscle group for 5 seconds, then release\n"
                "• Notice the difference between tension and relaxation\n"
                "• Move slowly upward: feet → legs → stomach → hands → arms → shoulders → face\n\n"
                "This signals to your body that it's safe to relax."
            ),
        },
    },
    "loneliness": {
        "opener": [
            "Feeling alone, especially when it feels like no one understands, is really painful.",
            "Loneliness is hard, even when there are people around. I'm here right now.",
        ],
        "technique": {
            "name": "Small Connection Step",
            "description": (
                "Loneliness can create a cycle where it feels harder to reach out the "
                "longer it goes on. One small, low-pressure step:\n"
                "• Send one message to someone - even just 'thinking of you'\n"
                "• You don't need a reason or a long conversation\n"
                "• If that feels like too much today, that's okay too - be gentle with yourself"
            ),
        },
    },
    "anger": {
        "opener": [
            "It makes sense to feel frustrated - that's a valid response.",
            "Anger often shows up when something important feels threatened or unfair.",
        ],
        "technique": {
            "name": "STOP Technique",
            "description": (
                "• STOP what you're doing\n"
                "• TAKE a breath\n"
                "• OBSERVE what you're feeling and thinking, without judgment\n"
                "• PROCEED with intention, not just reaction\n\n"
                "This creates a small gap between the feeling and what you do next."
            ),
        },
    },
    "greeting": {
        "opener": ["Hi there. I'm glad you're here. How are you feeling today?"],
        "technique": None,
    },
    "general": {
        "opener": [
            "Thank you for sharing that with me. Tell me more about what's on your mind.",
            "I'm listening. What's going on for you right now?",
        ],
        "technique": None,
    },
}


def generate_response(intent: str, sentiment_label: str) -> dict:
    """
    Builds a full chatbot response: an empathetic opener + (if relevant)
    an evidence-based technique the user can try right now.
    """
    entry = RESPONSE_LIBRARY.get(intent, RESPONSE_LIBRARY["general"])
    opener = random.choice(entry["opener"])
    technique = entry["technique"]

    return {
        "opener": opener,
        "technique": technique,  # None for greeting/general - just conversational
    }