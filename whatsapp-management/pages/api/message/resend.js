// pages/api/message/resend.js
import axios from 'axios';
// import prisma from '../../../lib/prisma'; // if you need to fetch existing message

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { messageId } = req.body; // The original message to be resent
  if (!messageId) {
    return res.status(400).json({ error: 'messageId is required' });
  }

  try {
    // Example: get the existing message from your DB (if you store the content)
    // const existingMessage = await prisma.message.findUnique({ where: { messageId } });
    // if (!existingMessage) throw new Error('Original message not found');

    // For demonstration, we'll just assume you pass in new content
    const content = req.body.content || 'Resending original content...';
    const recipientPhoneNumber = req.body.recipientPhoneNumber; 
    // ... or retrieve from existingMessage if needed

    const response = await axios.post(
      `${process.env.WHATSAPP_API_BASE_URL}/messages`,
      {
        messaging_product: 'whatsapp',
        to: recipientPhoneNumber,
        type: 'text',
        text: { body: content },
      },
      {
        headers: {
          Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}`,
          'Content-Type': 'application/json',
        },
      }
    );

    return res.status(200).json({
      success: true,
      resendResponse: response.data,
    });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}
