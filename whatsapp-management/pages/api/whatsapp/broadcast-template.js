// pages/api/whatsapp/broadcast-template.js
import axios from 'axios';
import prisma from '../../../lib/prisma';

export default async function handler(req, res) {
  
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  console.log("Broadcast-Template",req.body);

  const { groupId, templateName, templateLanguage, templateVariables } = req.body;


  if (!groupId || !templateName || !templateLanguage) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  try {
    
    
    // Fetch participants
    const participants = await prisma.groupParticipant.findMany({
      where: { groupId: Number(groupId) },
      include: { participant: true }
    });



    // Send template messages to each participant
    const results = [];
    for (const p of participants) {
      const toNumber = p.participant.phoneNumber;

      console.log('Broadcast Template :: ', toNumber, templateLanguage, templateVariables ,templateName );
      const response = await axios.post(
        `${process.env.WHATSAPP_API_BASE_URL}/${process.env.WHATSAPP_CLOUD_API_PHONE_NUMBER_ID}/messages`,
        {
          messaging_product: 'whatsapp',
          to: toNumber,
          type: 'template',
          template: {
            name: templateName,
            language: { code: templateLanguage },
            components: [
              {
                type: 'body',
                parameters: templateVariables
              }
            ]
          }
        },
        {
          headers: {
            Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}`,
            'Content-Type': 'application/json'
          }
        }
      );

      console.log("Broadcast Template:", response.data);

      results.push(response.data);
    }

    return res.status(200).json({ status: 'Template broadcast sent', details: results });
  } catch (error) {
    console.log(error.stack);
    console.error(error);
    return res.status(500).json({ error: error.message });
  }
}
