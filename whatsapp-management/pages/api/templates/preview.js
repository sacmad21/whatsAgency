import axios from 'axios';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { template_name, language, variables } = req.body;
    try {
      const response = await axios.post(
        `${process.env.WHATSAPP_API_BASE_URL}/message_templates/preview`,
        {
          template_name,
          language,
          components: variables,
        },
        {
          headers: {
            Authorization: `Bearer ${process.env.WHATSAPP_API_TOKEN}`,
            'Content-Type': 'application/json',
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
