// pages/api/message/deleteMessage.js
import axios from 'axios';

export default async function handler(req, res) {
  if (req.method !== 'DELETE') {

    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  // const { messageId } = req.query; // e.g. /api/message/deleteMessage?messageId=xxxx

  const messageId = "wamid.HBgMOTE3NjY2ODE5NDY4FQIAERgSQUNCOTI5NzE2REQyODQ2OERFAA=="

  if (!messageId) {
    return res.status(400).json({ error: 'messageId is required' });
  }


  console.log("Deleting Message ::", messageId)
  try {
    const response = await axios.delete(

      `${process.env.WHATSAPP_API_BASE_URL}/${process.env.WHATSAPP_CLOUD_API_PHONE_NUMBER_ID}/messages/${messageId}`,
      {
        headers: {
          Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}`,
        },
      }
    );



    return res.status(200).json({ success: true, deleteResponse: response.data });
  } catch (err) {
    console.log(err.stack);
    return res.status(500).json({ error: err.message });
  }
}
