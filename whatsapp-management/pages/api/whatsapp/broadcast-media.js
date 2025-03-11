// pages/api/whatsapp/broadcast-media.js
import axios from 'axios';
import prisma from '../../../lib/prisma';
import fs from 'fs';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { groupId, mediaPath, mediaType, caption } = req.body;

  if (!groupId || !mediaPath || !mediaType) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  try {
    // Upload media to WhatsApp API
    const mediaFile = fs.createReadStream(mediaPath);
    const uploadResponse = await axios.post(
      `${process.env.WHATSAPP_API_BASE_URL}/${process.env.WHATSAPP_API_VERSION}/${process.env.WABA_PHONE_NUMBER_ID}/media`,
      mediaFile,
      {
        headers: {
          Authorization: `Bearer ${process.env.WABA_CLOUD_API_TOKEN}`,
          'Content-Type': 'multipart/form-data'
        }
      }
    );

    const mediaId = uploadResponse.data.id;

    // Fetch participants
    const participants = await prisma.groupParticipant.findMany({
      where: { groupId: Number(groupId) },
      include: { participant: true }
    });

    // Send media messages to each participant
    const results = [];
    for (const p of participants) {
      const toNumber = p.participant.phoneNumber;
      const response = await axios.post(
        `${process.env.WHATSAPP_API_BASE_URL}/${process.env.WHATSAPP_API_VERSION}/${process.env.WABA_PHONE_NUMBER_ID}/messages`,
        {
          messaging_product: 'whatsapp',
          to: toNumber,
          type: mediaType,
          [mediaType]: { id: mediaId, caption }
        },
        {
          headers: {
            Authorization: `Bearer ${process.env.WABA_CLOUD_API_TOKEN}`,
            'Content-Type': 'application/json'
          }
        }
      );
      results.push(response.data);
    }

    return res.status(200).json({ status: 'Media broadcast sent', details: results });
  } catch (error) {
    console.error(error);
    return res.status(500).json({ error: error.message });
  }
}
