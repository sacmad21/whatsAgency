// pages/api/groups/index.js
import prisma from '../../../lib/prisma';

export default async function handler(req, res) {
  try {
    if (req.method === 'GET') {
      // Get all groups, including their creator and participants count
      const groups = await prisma.group.findMany({
        include: {
          creator: true,
          participants: true
        }
      });
      return res.status(200).json(groups);
    }

    if (req.method === 'POST') {
      console.log("Adding the group", req.body);
      const { groupId, name, description, createdBy } = req.body;
      const newGroup = await prisma.group.create({
        data: {
          groupId,
          name,
          description,
          createdBy
        },
        include: {
          creator: true,
          participants: true
        }
      });
      return res.status(201).json(newGroup);
    }

    return res.status(405).json({ error: 'Method not allowed' });
  } catch (error) {
    console.log(error.stack);
    console.error(error);
    return res.status(500).json({ error: error.message });
  }
}
