import prisma from '../../../lib/prisma';

export default async function handler(req, res) {
  if (req.method === 'PUT') {
    const { id, country, conversationPrice, messagePrice } = req.body;

    try {
      const pricing = await prisma.pricing.update({
        where: { id },
        data: { country, conversationPrice, messagePrice },
      });
      res.status(200).json(pricing);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  } else {
    res.setHeader('Allow', ['PUT']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
