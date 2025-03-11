// /pages/api/phoneNumber/[id].js

import { PrismaClient } from '@prisma/client';
const prisma = new PrismaClient();

export default async function handler(req, res) {
  const { id } = req.query;

  try {
    if (req.method === 'GET') {
      const phoneNumber = await prisma.phoneNumber.findUnique({
        where: { id: Number(id) },
      });
      if (!phoneNumber) return res.status(404).json({ error: 'Not found' });
      return res.status(200).json(phoneNumber);
    }

    if (req.method === 'PUT') {
      const { phoneNumber, status, twoStepVerificationStatus } = req.body;
      const updated = await prisma.phoneNumber.update({
        where: { id: Number(id) },
        data: {
          phoneNumber,
          status,
          twoStepVerificationStatus
        },
      });
      return res.status(200).json(updated);
    }

    if (req.method === 'DELETE') {
      await prisma.phoneNumber.delete({
        where: { id: Number(id) },
      });
      return res.status(204).send('');
    }

    return res.status(405).send('Method Not Allowed');
  } catch (error) {
    console.error(error);
    return res.status(500).json({ error: error.message });
  }
}
