import prisma from '../../../lib/prisma';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    const contacts = await prisma.contact.findMany();
    return res.status(200).json(contacts);
  }

  if (req.method === 'POST') {
    const data = req.body;
    const newContact = await prisma.contact.create({ data });
    return res.status(201).json(newContact);
  }

  res.setHeader('Allow', ['GET', 'POST']);
  res.status(405).end(`Method ${req.method} Not Allowed`);
}

