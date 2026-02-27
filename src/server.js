import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import { apiRouter } from './routes/api.js';

const app = express();
const PORT = process.env.PORT || 4000;

app.use(cors({ origin: true }));
app.use(express.json());

app.use('/api', apiRouter);

app.get('/health', (req, res) => {
  res.json({ ok: true, message: 'API is running' });
});

app.listen(PORT, () => {
  console.log(`Backend running at http://localhost:${PORT}`);
});
