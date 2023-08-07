const express = require('express');
const process = require('process');
const app = express();

app.get('/api/test', (req, res) => {
  res.json({ status: 'ok', remarks: 'Seems like the app is working!' });
});

const port = process.env['PORT'] || 3000;
console.log('Starting server...');

app.listen(port, () => {
  console.log('Server is now listening...');
});
