// pages/api/groups/[id].js
import prisma from '../../../lib/prisma';

export default async function handler(req, res) {
  const { id } = req.query;

  try {
    if (req.method === 'GET') {
      const group = await prisma.group.findUnique({
        where: { id: Number(id) },
        include: { creator: true, participants: true }
      });
      return res.status(200).json(group);
    }

    if (req.method === 'PUT') {
      const { groupId, name, description, createdBy } = req.body;
      const updatedGroup = await prisma.group.update({
        where: { id: Number(id) },
        data: {
          groupId,
          name,
          description,
          createdBy
        },
        include: { creator: true, participants: true }
      });
      return res.status(200).json(updatedGroup);
    }

    if (req.method === 'DELETE') {
      await prisma.group.delete({
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
