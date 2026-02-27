import { Router } from 'express';

export const apiRouter = Router();

apiRouter.get('/hello', (req, res) => {
  res.json({ message: 'Hello from API!' });
});

apiRouter.get('/ping', (req, res) => {
  res.json({ pong: Date.now() });
});
