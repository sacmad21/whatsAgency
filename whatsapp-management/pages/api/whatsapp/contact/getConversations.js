import axios from 'axios';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    const { phoneNumber } = req.query;

    try {
      const response = await axios.get(
        `${process.env.WHATSAPP_API_URL}/conversations`,
        {
          headers: {
            Authorization: `Bearer ${process.env.WHATSAPP_ACCESS_TOKEN}`,
          },
          params: {
            phone_number: phoneNumber,
          },
        }
      );
      res.status(200).json(response.data);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  } else {
    res.setHeader('Allow', ['GET']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
