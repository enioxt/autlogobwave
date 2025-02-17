const express = require('express');
const { create } = require('@wppconnect-team/wppconnect');
const cors = require('cors');
const sharp = require('sharp');

const app = express();
const PORT = process.env.PORT || 8080;

// Variável global para armazenar o QR Code
let qrCode = '';

app.use(cors());
app.use(express.json());

// Rota principal com HTML básico
app.get('/', (req, res) => {
  res.send(`
    <html>
      <head>
        <title>WhatsApp Bot</title>
      </head>
      <body>
        <h1>Status do Bot WhatsApp</h1>
        ${qrCode ? `<img src="${qrCode}" alt="QR Code"/>` : '<p>Aguardando QR Code...</p>'}
        <p>Status: ${qrCode ? 'Aguardando conexão' : 'Iniciando...'}</p>
      </body>
    </html>
  `);
});

// Rota para obter o QR Code atual
app.get('/qrcode', (req, res) => {
  if (qrCode) {
    res.json({ qrcode: qrCode });
  } else {
    res.status(404).json({ message: 'QR Code não disponível' });
  }
});

async function startAutomation() {
  try {
    const client = await create({
      session: 'autolog-session',
      puppeteer: {
        headless: true,
        args: [
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage'
        ]
      },
      catchQR: (base64Qr) => {
        qrCode = base64Qr; // Armazena o QR Code
        console.log('QR Code atualizado!');
      },
      statusFind: (statusSession) => {
        console.log(`Status: ${statusSession}`);
      }
    });

    // Resto do seu código...
  } catch (error) {
    console.error('Erro:', error);
  }
}

app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
  startAutomation();
});
