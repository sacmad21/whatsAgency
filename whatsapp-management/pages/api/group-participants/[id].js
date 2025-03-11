// pages/api/group-participants/[id].js
import prisma from '../../../lib/prisma';

export default async function handler(req, res) {
  const { id } = req.query;

  try {
    if (req.method === 'GET') {
      const participant = await prisma.groupParticipant.findUnique({
        where: { id: Number(id) },
        include: { group: true, participant: true }
      });
      return res.status(200).json(participant);
    }

    if (req.method === 'PUT') {
      const { groupId, participantId, role } = req.body;
      const updatedParticipant = await prisma.groupParticipant.update({
        where: { id: Number(id) },
        data: {
          groupId,
          participantId,
          role
        },
        include: { group: true, participant: true }
      });
      return res.status(200).json(updatedParticipant);
    }

    if (req.method === 'DELETE') {
      await prisma.groupParticipant.delete({
        where: { id: Number(id) }
      });
      return res.status(204).end();
    }

    return res.status(405).json({ error: 'Method not allowed' });
  } catch (error) {
    console.error(error);
    return res.status(500).json({ error: error.message });
  }
}
