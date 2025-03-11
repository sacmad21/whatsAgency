// /pages/api/phoneNumber/whatsapp.js
import axios from 'axios';

export default async function handler(req, res) {
  // e.g., POST /api/phoneNumber/whatsapp
  // body: { id, to, message }
  if (req.method !== 'POST') {
    return res.status(405).send('Method Not Allowed');
  }

  const { id, message, tonumber } = req.body;
  console.log("Sending message");
  console.log(id,message,tonumber);
  try {
    // Retrieve phoneNumber record if needed
    // Example: const phoneRecord = await prisma.phoneNumber.findUnique({ where: { id } });
    // Then pass phoneRecord.phoneNumber to the actual WA send message

    // Make a WhatsApp API call with the .env credentials
    const result = await axios.post(
      `${process.env.WHATSAPP_API_BASE_URL}/${process.env.WHATSAPP_CLOUD_API_PHONE_NUMBER_ID}/messages`,
      {
        messaging_product: 'whatsapp',
        to: tonumber,
        text: { body: message },
      },
      {
        headers: {
          Authorization: `Bearer ${process.env.WHATSAPP_API_TOKEN}`,
          'Content-Type': 'application/json',
        },
      }
    );

    return res.status(200).json({ success: true, data: result.data });
  } catch (error) {
    console.error(error);
    return res.status(500).json({ error: error.response?.data || error.message });
  }
}
