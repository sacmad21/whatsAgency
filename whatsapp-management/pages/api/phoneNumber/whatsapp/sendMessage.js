// /pages/api/phoneNumber/whatsapp/sendMessage.js
import { PrismaClient } from '@prisma/client';
import axios from 'axios';

const prisma = new PrismaClient();

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { id, message } = req.body;



  try {
    // 1. Fetch the receiverPhoneNumber phone number
    const receiverPhoneNumber = await prisma.phoneNumber.findUnique({
      where: { id: Number(id) },
    });

    if (!receiverPhoneNumber) {
      return res.status(404).json({ error: 'receiverPhoneNumber PhoneNumber not found.' });
    }

    const sender =  Number(process.env.WHATSAPP_CLOUD_API_PHONE_NUMBER_ID) ;

    // 2. Make the API call to WhatsApp
    const response = await axios.post(
      `${process.env.WHATSAPP_API_BASE_URL}/${process.env.WHATSAPP_CLOUD_API_PHONE_NUMBER_ID}/messages`,
      {
        messaging_product: 'whatsapp',
        to: receiverPhoneNumber.phoneNumber, // Recipient phone number
        text: { body: message }, // Message content
      },
      {
        headers: {
          Authorization: `Bearer ${process.env.WHATSAPP_API_TOKEN}`,
          'Content-Type': 'application/json',
        },
      }
    );

    const messageId = response.data.messages[0]?.id || 'unknown';

    // 3. Log the message into the Message table
    await prisma.message.create({
      data: {
        messageId: messageId,
        type: 'TEXT', // Assuming this is a text message
        content: message,
        status: 'SENT', // Assuming it was successfully sent
        direction: 'OUTGOING',
        senderPhoneNumberId: 6, // Sender's PhoneNumber ID
        recipientPhoneNumberId: id, // You may need to change this to the recipient's ID
      },
    });

    return res.status(200).json({ success: true, data: response.data });
  } catch (error) {
    console.error(error);
    return res.status(500).json({
      error: error.response?.data || error.message || 'Unknown error occurred.',
    });
  }
}
