# MindSpace — AI-Powered Mental Health Support Chatbot

A full-stack mental health support chatbot that uses NLP and rule-based ML to provide immediate, evidence-based emotional support, crisis detection, and coping techniques — anonymously and at no cost to the user.

**Live Demo:** https://mental-health-chatbot-zeta-eight.vercel.app

> Note: The backend runs on free-tier hosting, so the first message after inactivity may take 30–50 seconds while the server wakes up. Subsequent messages are fast.

---

## What it does

MindSpace lets users describe how they're feeling in plain language and responds with:
- An empathetic, context-aware reply
- A relevant evidence-based coping technique (CBT reframing, grounding exercises, breathing techniques, etc.)
- Immediate crisis-line resources if the message indicates a mental health crisis — this check runs before anything else and overrides all other logic

## Why I built this

Many people don't seek mental health support due to stigma, cost, or lack of access. This project explores how NLP and a thoughtfully designed rule-based safety system can provide immediate, anonymous, evidence-based support as a first line of help — while being explicit about what it can't replace.

## Architecture

React (Vercel) → Node.js/Express (Render) → Python/FastAPI (Render) → MongoDB Atlas

- **Frontend (React + Vite)**: chat interface, session handling, crisis-state styling
- **Backend (Node.js/Express)**: routes requests between frontend and ML service, persists anonymized conversations to MongoDB
- **ML Service (Python/FastAPI)**: crisis detection, sentiment analysis, intent classification, response generation
- **Database (MongoDB Atlas)**: stores conversations by anonymous session ID — no accounts, no personal data

I split the ML logic into its own microservice so it can scale or be swapped independently of the main backend — for example, replacing the rule-based intent classifier with a fine-tuned transformer model later wouldn't require touching the Node backend at all.

## Key design decisions

- **Crisis detection is rule-based, not ML-based.** This was a deliberate choice: false negatives on crisis-level language carry serious consequences, and keyword matching is predictable, auditable, and fast, whereas a probabilistic model's failure modes are harder to guarantee against. Crisis detection always runs first and short-circuits the rest of the response pipeline.
- **No user accounts.** Sessions are anonymous and ephemeral — this protects user privacy for a sensitive use case, at the cost of persistent chat history across visits (an intentional trade-off).
- **Sentiment analysis uses VADER**, which is tuned for informal/conversational text rather than formal writing — a better fit for chat messages than a general-purpose sentiment model.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, CSS |
| Backend | Node.js, Express, Mongoose |
| ML Service | Python, FastAPI, VADER Sentiment |
| Database | MongoDB Atlas |
| Deployment | Vercel (frontend), Render (backend + ML service) |

## Known Limitations

- **Crisis detection is keyword-based**, so it can miss unusually phrased crisis language and may false-positive on things like song lyrics or hypothetical statements. In a production/clinical setting, this list should be reviewed and expanded by mental health professionals.
- **Intent classification is rule-based**, not a trained ML model. A natural next step would be fine-tuning a transformer (e.g. DistilBERT) on labeled conversational data for more nuanced intent detection.
- **Free-tier hosting** means the backend and ML service spin down after inactivity, causing a delay on the first request.
- **This is a portfolio/educational project, not a clinically validated tool**, and is not a substitute for professional mental healthcare.

## Future Improvements

- Fine-tuned ML model for intent classification instead of keyword matching
- Voice input/output
- Multi-language support
- Admin dashboard for anonymized usage analytics (mood trends, common topics)

## Running Locally

Clone the repo, then set up each service in its own terminal:

**ML Service:**
1. `cd ml-service`
2. `python -m venv venv`
3. `source venv/Scripts/activate` (or `venv/bin/activate` on Mac/Linux)
4. `pip install -r requirements.txt`
5. `python main.py`

**Backend** (in a new terminal):
1. `cd backend`
2. `npm install`
3. Create a `.env` file with `PORT`, `MONGO_URI`, and `ML_SERVICE_URL`
4. `node server.js`

**Frontend** (in a new terminal):
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Author

Anuj Diwakar