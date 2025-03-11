// pages/api/phonenumbers/whatsapp/twoStepVerification.js

import axios from 'axios';

export default async function handler(req, res) {
  const { method } = req;
  try {
    if (method === 'POST') {
      // Enable 2FA
      const response = await axios.post(
        `${process.env.WHATSAPP_API_URL}/settings/two_step_verification`,
        {},
        {
          headers: {
            Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}`,
            'Content-Type': 'application/json'
          }
        }
      );
      return res.status(200).json(response.data);
    } else if (method === 'DELETE') {
      // Disable 2FA
      const response = await axios.delete(
        `${process.env.WHATSAPP_API_URL}/settings/two_step_verification`,
        {
          headers: {
            Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}`,
          }
        }
      );
      return res.status(200).json(response.data);
    } else {
      return res.status(405).json({ error: 'Method not allowed' });
    }
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
}
