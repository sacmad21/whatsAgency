// pages/api/group-participants/index.js
import prisma from '../../../lib/prisma';

export default async function handler(req, res) {
  try {


    if (req.method === 'GET') {
      const { groupId } = req.query; // Extract groupId from the request query

      try {
        const participants = await prisma.groupParticipant.findMany({
          where: {
            groupId: Number(groupId),           },
          include: { group: true, participant: true }, // Include related group and participant details
        });

        return res.status(200).json(participants);
      } catch (error) {
        console.error('Error fetching participants:', error);
        return res.status(500).json({ error: error.message });
      }
    }

    if (req.method === 'POST') {
      console.log("Group Participant body :", req.body);
      const { groupId, participantId, role } = req.body;
      const newParticipant = await prisma.groupParticipant.create({
        data: {
          groupId,
          participantId,
          role
        },
        include: { group: true, participant: true }
      });
      return res.status(201).json(newParticipant);
    }

    return res.status(405).json({ error: 'Method not allowed' });
  } catch (error) {

    console.error(error.stack);
    return res.status(500).json({ error: error.message });
  }
}
