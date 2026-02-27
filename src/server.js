import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import { apiRouter } from './routes/api.js';

const app = express();
const PORT = process.env.PORT || 4000;

// Allow all origins for dev; specify in prod as needed
app.use(cors({ origin: true, credentials: true }));
app.use(express.json());

// Minimal /api/hello endpoint for compatibility with frontend
app.get('/api/hello', (req, res) => {
  res.json({ message: 'Hello from RPM backend!' });
});

app.use('/api', apiRouter);

// Health endpoint as required by frontend
app.get('/health', (req, res) => {
  res.json({ ok: true, status: 'healthy', message: 'API is running' });
});

app.listen(PORT, () => {
  console.log(`Backend running at http://localhost:${PORT}`);
});
