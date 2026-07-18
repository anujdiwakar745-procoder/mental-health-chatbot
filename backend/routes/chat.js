/**
 * Chat Route
 * -----------
 * Receives a user message, forwards it to the Python ML service,
 * saves the exchange to MongoDB, and returns the reply.
 */

const express = require('express');
const axios = require('axios');
const Conversation = require('../models/Conversation');
const router = express.Router();

const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://localhost:8000';

router.post('/', async (req, res) => {
  const { text, sessionId } = req.body;

  if (!text || !text.trim()) {
    return res.status(400).json({ error: 'Message text is required' });
  }

  // Use a provided sessionId, or fall back to "anonymous" if the
  // frontend hasn't been updated to send one yet.
  const finalSessionId = sessionId || 'anonymous';

  try {
    const mlResponse = await axios.post(`${ML_SERVICE_URL}/chat`, { text });
    const data = mlResponse.data;

    // Save the exchange - don't let a DB save failure break the chat response.
    try {
      await Conversation.create({
        sessionId: finalSessionId,
        userMessage: text,
        botReply: data.reply,
        intent: data.intent,
        sentimentLabel: data.sentiment_label,
        isCrisis: data.is_crisis,
      });
    } catch (dbErr) {
      console.error('Failed to save conversation:', dbErr.message);
    }

    res.json(data);
  } catch (error) {
    console.error('Error calling ML service:', error.message);
    res.status(502).json({
      error: 'Could not reach the AI service. Please try again in a moment.',
    });
  }
});

module.exports = router;