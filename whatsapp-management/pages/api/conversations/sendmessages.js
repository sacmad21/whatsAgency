import axios from 'axios';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { phoneNumber, messageType, text, conversationType } = req.body;

    // Validate required fields
    if (!phoneNumber || !messageType || !text || !conversationType) {
      res.status(400).json({ error: 'phoneNumber, messageType, text, and conversationType are required.' });
      return;
    }

    try {
      const response = await axios.post(
        `${process.env.WHATSAPP_API_BASE_URL}/v1/messages`,
        {
          messaging_product: 'whatsapp',
          to: phoneNumber,
          type: messageType,
          text: { body: text },
          conversationType,
        },
        {
          headers: { Authorization: `Bearer ${process.env.WHATSAPP_API_TOKEN}` },
        }
      );
      res.status(200).json(response.data);
    } catch (error) {
      console.error('Error sending message:', error);
      res.status(500).json({ error: error.message });
    }
  } else {
    res.status(405).send('Method Not Allowed');
  }
}
