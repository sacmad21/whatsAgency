export default async function handler(req, res) {
    if (req.method === 'POST') {
      const event = req.body;
  
      // Log or process the incoming event
      console.log('Webhook Event Received:', event);
  
      // Example: Save the event to a database
      // await prisma.webhooks.create({ data: { payload: JSON.stringify(event) } });
  
      res.status(200).send('Event Received');
    } else if (req.method === 'GET') {
      // Verification Challenge for WhatsApp
      const mode = req.query['hub.mode'];
      const token = req.query['hub.verify_token'];
      const challenge = req.query['hub.challenge'];
  
      if (mode && token === process.env.WHATSAPP_VERIFY_TOKEN) {
        res.status(200).send(challenge);
      } else {
        res.status(403).send('Verification Failed');
      }
    } else {
      res.status(405).send('Method Not Allowed');
    }
  }
  