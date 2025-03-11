import axios from 'axios';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    const { messageId } = req.query;

    // Validate required fields
    if (!messageId) {
      res.status(400).json({ error: 'messageId is required.' });
      return;
    }

    try {
      const response = await axios.get(
        `${process.env.WHATSAPP_API_BASE_URL}/v1/messages/${messageId}`,
        {
          headers: { Authorization: `Bearer ${process.env.WHATSAPP_API_TOKEN}` },
        }
      );
      res.status(200).json(response.data);
    } catch (error) {
      console.error('Error fetching message status:', error);
      res.status(500).json({ error: error.message });
    }
  } else {
    res.status(405).send('Method Not Allowed');
  }
}
