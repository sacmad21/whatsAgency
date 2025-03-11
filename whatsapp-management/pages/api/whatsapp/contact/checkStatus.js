import axios from 'axios';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { phoneNumbers } = req.body; // Array of phone numbers
    try {
      const response = await axios.post(
        `${process.env.WHATSAPP_API_URL}/contacts`,
        { blocking: "wait", contacts: phoneNumbers },
        {
          headers: {
            Authorization: `Bearer ${process.env.WHATSAPP_ACCESS_TOKEN}`,
          },
        }
      );
      res.status(200).json(response.data);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  } else {
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
