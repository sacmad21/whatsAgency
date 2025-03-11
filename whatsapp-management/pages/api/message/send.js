// pages/api/message/send.js
import axios from 'axios';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { recipientPhoneNumber, content, type } = req.body;

  try {
    const response = await axios.post(
      `${process.env.WHATSAPP_API_BASE_URL}/${process.env.WHATSAPP_CLOUD_API_PHONE_NUMBER_ID}/messages`,
      {
        messaging_product: 'whatsapp',
        to: recipientPhoneNumber,
        type: type || 'text', // e.g., 'text'
        text: { body: content },
      },
      {
        headers: {
          Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}`,
          'Content-Type': 'application/json',
        },
      }
    );

    // Save to DB if needed (e.g. via Prisma)
    // e.g.: await prisma.message.create({ data: { ... } });

    console.log("Response Send Msg", response.data);

    return res.status(200).json({
      success: true,
      message: 'Message sent successfully!',
      apiResponse: response.data,
    });


  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}
