/**
 * Conversation Model
 * --------------------
 * Defines the structure for storing chat exchanges in MongoDB.
 *
 * PRIVACY NOTE: We store a randomly generated sessionId instead of any
 * personal user info (no names, emails, or accounts) - this keeps the
 * data anonymized, which matters a lot for a mental health app.
 */

const mongoose = require('mongoose');

const conversationSchema = new mongoose.Schema({
  sessionId: {
    type: String,
    required: true,
  },
  userMessage: {
    type: String,
    required: true,
  },
  botReply: {
    type: String,
    required: true,
  },
  intent: {
    type: String,
    default: 'general',
  },
  sentimentLabel: {
    type: String,
    default: 'neutral',
  },
  isCrisis: {
    type: Boolean,
    default: false,
  },
  createdAt: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model('Conversation', conversationSchema);