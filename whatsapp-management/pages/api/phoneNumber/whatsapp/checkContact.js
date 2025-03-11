// pages/api/phonenumbers/whatsapp/checkContact.js

import axios from 'axios';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }
  const { phoneNumber } = req.body;

  try {
    const response = await axios.post(
      `${process.env.WHATSAPP_API_URL}/contacts`,
      {
        messaging_product: 'whatsapp',
        contacts: [ phoneNumber ]
      },
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
