"""
Mental Health Chatbot - ML Service
-----------------------------------
This FastAPI service handles NLP tasks: crisis detection, sentiment
analysis, and (later) intent classification.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from utils.crisis_detector import detect_crisis, CRISIS_RESOURCES
from utils.sentiment_analyzer import analyze_sentiment
from utils.intent_classifier import classify_intent
from utils.response_generator import generate_response

app = FastAPI(
    title="Mental Health Chatbot - ML Service",
    description="Handles crisis detection, sentiment analysis, and intent classification",
    version="0.1.0",
)

# Allows your Node backend and React frontend to call this service.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class MessageRequest(BaseModel):
    text: str


class AnalyzeResponse(BaseModel):
    is_crisis: bool
    severity: str
    crisis_message: str | None = None
    crisis_resources: list | None = None
    sentiment: dict
    intent: str
    
class ChatResponse(BaseModel):
    is_crisis: bool
    reply: str
    technique: dict | None = None
    intent: str
    sentiment_label: str

@app.get("/", response_model=HealthResponse)
def root():
    return HealthResponse(status="ok", service="ml-service", version="0.1.0")


@app.get("/health", response_model=HealthResponse)
def health_check():
    """Used by your backend and deployment platform to confirm this service is alive."""
    return HealthResponse(status="ok", service="ml-service", version="0.1.0")


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_message(payload: MessageRequest):
    """
    Analyzes an incoming user message for crisis indicators, sentiment,
    and intent. Crisis check happens first and takes priority.
    """
    crisis_result = detect_crisis(payload.text)
    sentiment_result = analyze_sentiment(payload.text)
    intent_result = classify_intent(payload.text)

    if crisis_result["is_crisis"]:
        severity = crisis_result["severity"]
        crisis_info = CRISIS_RESOURCES.get(severity, CRISIS_RESOURCES["moderate"])
        return AnalyzeResponse(
            is_crisis=True,
            severity=severity,
            crisis_message=crisis_info["message"],
            crisis_resources=crisis_info["resources"],
            sentiment=sentiment_result,
            intent=intent_result["intent"],
        )

    return AnalyzeResponse(
        is_crisis=False,
        severity="none",
        sentiment=sentiment_result,
        intent=intent_result["intent"],
    )
    
@app.post("/chat", response_model=ChatResponse)
def chat(payload: MessageRequest):
    """
    Full conversational endpoint - this is what your frontend/backend
    should call. Combines crisis detection, sentiment, intent, and
    generates an actual reply with an evidence-based technique.
    """
    crisis_result = detect_crisis(payload.text)

    if crisis_result["is_crisis"]:
        severity = crisis_result["severity"]
        crisis_info = CRISIS_RESOURCES.get(severity, CRISIS_RESOURCES["moderate"])
        resource_lines = "\n".join(
            f"• {r['name']}: {r['contact']}" for r in crisis_info["resources"]
        )
        reply = f"{crisis_info['message']}\n\n{resource_lines}"
        return ChatResponse(
            is_crisis=True,
            reply=reply,
            technique=None,
            intent="crisis",
            sentiment_label="n/a",
        )

    sentiment_result = analyze_sentiment(payload.text)
    intent_result = classify_intent(payload.text)
    response = generate_response(intent_result["intent"], sentiment_result["label"])

    return ChatResponse(
        is_crisis=False,
        reply=response["opener"],
        technique=response["technique"],
        intent=intent_result["intent"],
        sentiment_label=sentiment_result["label"],
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)