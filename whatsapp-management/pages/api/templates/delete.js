import axios from 'axios';

export default async function handler(req, res) {
  if (req.method === 'DELETE') {
    const { template_name } = req.body;
    try {
      const response = await axios.delete(
        `${process.env.WHATSAPP_API_BASE_URL}/message_templates/${template_name}`,
        {
          headers: {
            Authorization: `Bearer ${process.env.WHATSAPP_API_TOKEN}`,
          },
        }
      );
      res.status(200).json(response.data);
    } catch (error) {
      res.status(500).json({ error: error.response?.data || error.message });
    }
  } else {
    res.status(405).send('Method Not Allowed');
  }
}
