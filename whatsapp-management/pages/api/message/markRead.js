// pages/api/message/markRead.js
import axios from 'axios';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { messageId } = req.body; // Sent from client in JSON body

  if (!messageId) {
    return res.status(400).json({ error: 'messageId is required' });
  }

  try {
    const response = await axios.post(
      `${process.env.WHATSAPP_API_BASE_URL}/messages/${messageId}/read`,
      {},
      {
        headers: {
          Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}`,
          'Content-Type': 'application/json',
        },
      }
    );

    return res.status(200).json({
      success: true,
      readResponse: response.data,
    });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}
