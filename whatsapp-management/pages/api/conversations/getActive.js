import axios from 'axios';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    const { phoneNumber, conversationType } = req.query;

    try {
      const url = `${process.env.WHATSAPP_API_BASE_URL}/v1/conversations`;
      const response = await axios.get(url, {
        headers: { Authorization: `Bearer ${process.env.WHATSAPP_API_TOKEN}` },
        params: { to: phoneNumber, conversationType },
      });
      res.status(200).json(response.data);
    } catch (error) {
      console.error('Error fetching active conversations:', error);
      res.status(500).json({ error: error.message });
    }
  } else {
    res.status(405).send('Method Not Allowed');
  }
}
