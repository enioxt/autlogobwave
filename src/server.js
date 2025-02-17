const express = require('express');
const { create } = require('@wppconnect-team/wppconnect');
const cors = require('cors');
const path = require('path');
const { PythonShell } = require('python-shell');
const sharp = require('sharp');

const app = express();
const PORT = process.env.PORT || 8080;

// Configurações essenciais
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Rota raiz para verificação do servidor
app.get('/', (req, res) => {
  res.send('🤖 Serviço de Redimensionamento de Logos via WhatsApp');
});

// Função principal de automação
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
        console.log('⚠️ Escaneie o QR Code no WhatsApp Web!');
      },
      statusFind: (statusSession) => {
        console.log(`📱 Status da Conexão: ${statusSession}`);
      }
    });

    // Evento para mensagens de mídia
    client.onMessage(async (message) => {
      try {
        if (message.isMedia || message.isImage) {
          // Download da imagem original
          const mediaData = await client.downloadMedia(message);
          
          // Processamento da imagem
          const resizedImage = await sharp(Buffer.from(mediaData.data, 'base64'))
            .resize(800, 800, { fit: 'inside' })
            .toBuffer();

          // Envio da imagem redimensionada
          await client.sendImage(
            message.from,
            `data:${mediaData.mimetype};base64,${resizedImage.toString('base64')}`,
            'logo-redimensionada.png',
            '✅ Logo redimensionada com sucesso!'
          );
        }
      } catch (error) {
        console.error('❌ Erro no processamento:', error);
        await client.sendText(message.from, '😟 Não consegui processar a imagem. Tente novamente!');
      }
    });

    console.log('🚀 Automação pronta para receber mensagens!');
  } catch (error) {
    console.error('‼️ Falha crítica:', error);
    process.exit(1);
  }
}

// Inicialização do servidor
app.listen(PORT, () => {
  console.log(`🔥 Servidor rodando em: http://localhost:${PORT}`);
  startAutomation();
});
