import prisma from '../../../lib/prisma';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    try {
      // Fetch messages with necessary relations
      const messages = await prisma.message.findMany({
        include: {
          template: true, // Include template details if related
          media: true,    // Include media details if related
          senderPhoneNumber: {
            select: {
              id: true,
              phoneNumber: true,
            },
          },
          recipientPhoneNumber: {
            select: {
              id: true,
              phoneNumber: true,
            },
          },
        },
      });

      // Format the response for the DataTable
      const formattedMessages = messages.map((message) => ({
        id: message.id,
        messageId: message.messageId,
        type: message.type,
        content: message.content || 'N/A',
        status: message.status,
        direction: message.direction,
        senderPhoneNumber: message.senderPhoneNumber?.phoneNumber || 'N/A',
        recipientPhoneNumber: message.recipientPhoneNumber?.phoneNumber || 'N/A',
        createdAt: message.createdAt,
        updatedAt: message.updatedAt,
      }));

      res.status(200).json(formattedMessages);
    } catch (error) {
      console.error('Error fetching messages:', error);
      res.status(500).json({ error: 'Failed to fetch messages' });
    }
  } else {
    // Handle unsupported methods
    res.status(405).json({ error: 'Method Not Allowed' });
  }
}
