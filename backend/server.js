const dns = require('dns');
dns.setServers(['8.8.8.8', '8.8.4.4']);

require('dotenv').config();
const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

const chatRoute = require('./routes/chat');
app.use('/chat', chatRoute);

app.get('/', (req, res) => {
  res.json({ status: 'ok', service: 'backend', version: '0.1.0' });
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'backend', version: '0.1.0' });
});

mongoose
  .connect(process.env.MONGO_URI)
  .then(() => {
    console.log('Connected to MongoDB');
    app.listen(PORT, () => {
      console.log('Backend server running on http://localhost:' + PORT);
    });
  })
  .catch((err) => {
    console.error('MongoDB connection error:', err.message);
  });