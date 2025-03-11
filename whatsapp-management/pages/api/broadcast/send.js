import axios from 'axios';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { user_ids, content } = req.body; // user_ids is an array of user IDs
    try {
      // Fetch phone numbers of all users
      const users = await prisma.users.findMany({
        where: { user_id: { in: user_ids } },
        select: { phone: true },
      });

      // Send a message to each user
      const responses = await Promise.all(
        users.map((user) =>
          axios.post(
            'https://graph.facebook.com/v15.0/your-whatsapp-endpoint/messages',
            {
              messaging_product: 'whatsapp',
              to: user.phone,
              type: 'text',
              text: { body: content },
            },
            { headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` } }
          )
        )
      );

      res.status(200).json({ responses });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  } else {
    res.status(405).send('Method Not Allowed');
  }
}
