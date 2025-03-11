// pages/api/whatsapp/webhook.js
export default async function handler(req, res) {
    if (req.method === 'GET') {
      // Verification handshake for WhatsApp API webhook
      const VERIFY_TOKEN = process.env.WHATSAPP_VERIFY_TOKEN;
      const mode = req.query['hub.mode'];
      const token = req.query['hub.verify_token'];
      const challenge = req.query['hub.challenge'];
  
      if (mode && token) {
        if (mode === 'subscribe' && token === VERIFY_TOKEN) {
          console.log('WEBHOOK VERIFIED');
          return res.status(200).send(challenge);
        } else {
          return res.status(403).send('Forbidden');
        }
      }
    } else if (req.method === 'POST') {
      // Handle WhatsApp Webhook Events
      const body = req.body;
      console.log('Webhook Event:', JSON.stringify(body, null, 2));
  
      res.status(200).send('EVENT_RECEIVED');
    } else {
      res.setHeader('Allow', ['GET', 'POST']);
      res.status(405).end(`Method ${req.method} Not Allowed`);
    }
  }
  