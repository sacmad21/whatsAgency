import prisma from '../../../lib/prisma';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    try {
      // Set a cost threshold
      const costThreshold = 1000; // Example: $1000

      // Fetch total cost
      const totalCost = await prisma.conversations.aggregate({
        _sum: {
          pricing_amount: true,
        },
      });

      const currentCost = totalCost._sum.pricing_amount || 0;

      // Check if cost exceeds threshold
      if (currentCost > costThreshold) {
        res.status(200).json({
          alert: true,
          message: `Total conversation cost (${currentCost}) exceeds the threshold (${costThreshold}).`,
        });
      } else {
        res.status(200).json({
          alert: false,
          message: 'Costs are within the threshold.',
        });
      }
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  } else {
    res.status(405).send('Method Not Allowed');
  }
}
