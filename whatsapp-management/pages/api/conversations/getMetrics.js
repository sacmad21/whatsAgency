import axios from 'axios';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    const { conversationType } = req.query;

    try {
      const url = `${process.env.WHATSAPP_API_BASE_URL}/v1/metrics`;
      const response = await axios.get(url, {
        headers: { Authorization: `Bearer ${process.env.WHATSAPP_API_TOKEN}` },
        params: { conversationType },
      });
      res.status(200).json(response.data);
    } catch (error) {
      console.error('Error fetching metrics:', error);
      res.status(500).json({ error: error.message });
    }
  } else {
    res.status(405).send('Method Not Allowed');
  }
}
