import prisma from '../../../lib/prisma';

export default async function handler(req, res) {
  const { id } = req.query;

  if (req.method === 'GET') {
    const contact = await prisma.contact.findUnique({
      where: { id: parseInt(id) },
    });
    return res.status(200).json(contact);
  }

  if (req.method === 'PUT') {
    const data = req.body;
    const updatedContact = await prisma.contact.update({
      where: { id: parseInt(id) },
      data,
    });
    return res.status(200).json(updatedContact);
  }

  if (req.method === 'DELETE') {
    await prisma.contact.delete({
      where: { id: parseInt(id) },
    });
    return res.status(204).end();
  }

  res.setHeader('Allow', ['GET', 'PUT', 'DELETE']);
  res.status(405).end(`Method ${req.method} Not Allowed`);
}
