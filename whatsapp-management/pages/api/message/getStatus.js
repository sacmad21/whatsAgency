// pages/api/message/getStatus.js
import axios from 'axios';

export default async function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { messageId } = req.query; // e.g. /api/message/getStatus?messageId=xxxx

  if (!messageId) {
    return res.status(400).json({ error: 'messageId is required' });
  }

  try {
    const response = await axios.get(
      `${process.env.WHATSAPP_API_BASE_URL}/messages/${messageId}`,
      {
        headers: {
          Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}`,
        },
      }
    );

    return res.status(200).json({
      success: true,
      status: response.data,
    });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}
