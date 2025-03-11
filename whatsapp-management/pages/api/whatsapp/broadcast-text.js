// pages/api/whatsapp/broadcast-text.js
import axios from 'axios';
import prisma from '../../../lib/prisma';

export default async function handler(req, res) {

  console.log("Broadcast-Text", req.body);

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { groupId, messageText } = req.body;
  if (!groupId || !messageText) {
    return res.status(400).json({ error: 'Missing groupId or messageText' });
  }

  try {
    // 1. Fetch participants

    const participants = await prisma.groupParticipant.findMany({
      where: { groupId: Number(groupId) },
      include: { participant: true }
    });

    console.log("Participants::", participants);

    // 2. For each participant, send a text message via the WhatsApp API
    const results = [];
    for (const p of participants) {

      const toNumber = p.participant.phoneNumber; // e.g. '+1234567890'

      const sendResponse = await axios.post(
        `${process.env.WHATSAPP_API_BASE_URL}/${process.env.WHATSAPP_CLOUD_API_PHONE_NUMBER_ID}/messages`,
        {
          messaging_product: 'whatsapp',
          to: toNumber,
          text: { body: messageText },
          type: 'text'
        },
        {
          headers: {
            Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}`,
            'Content-Type': 'application/json'
          }
        }
      );

      console.log("Response::::::::::\n", sendResponse.data);
      results.push(sendResponse.data);
    }

    return res.status(200).json({ status: 'Broadcast sent', details: results });
  } catch (error) {
    console.error(error.stack);
    return res.status(500).json({ error: error.message });
  }
}
