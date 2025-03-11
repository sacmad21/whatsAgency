import prisma from '../../../lib/prisma';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    try {
      // Fetch active conversations
      const activeConversations = await prisma.conversations.count({
        where: {
          expiration_time: {
            gt: new Date(), // Expiration time greater than now
          },
        },
      });

      // Fetch total cost of conversations
      const totalCost = await prisma.conversations.aggregate({
        _sum: {
          pricing_amount: true,
        },
      });

      // Fetch conversations per category
      const categoryBreakdown = await prisma.conversations.groupBy({
        by: ['type'],
        _count: { type: true },
        _sum: { pricing_amount: true },
      });

      res.status(200).json({
        activeConversations,
        totalCost: totalCost._sum.pricing_amount || 0,
        categoryBreakdown,
      });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  } else {
    res.status(405).send('Method Not Allowed');
  }
}
