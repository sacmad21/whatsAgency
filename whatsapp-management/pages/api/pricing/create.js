import prisma from '../../../lib/prisma';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    console.log(req.body);
    const { country, conversationPrice, messagePrice } = req.body;

    try {
      const pricing = await prisma.pricing.create({
        data: { country, conversationPrice, messagePrice },
      });
      res.status(201).json(pricing);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  } else {
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
