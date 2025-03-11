// pages/api/phonenumbers/whatsapp/updateSettings.js

import axios from 'axios';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }
  const { phoneNumberId, settings } = req.body; // e.g., fallback values, callback URLs, etc.

  try {
    const response = await axios.post(
      `${process.env.WHATSAPP_API_URL}/phone_numbers/${phoneNumberId}`,
      settings,
      {
        headers: {
          Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}`,
          'Content-Type': 'application/json'
        }
      }
    );
    return res.status(200).json(response.data);
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
}
