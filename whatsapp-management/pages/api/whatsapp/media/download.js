// pages/api/whatsapp/media/download.js
import axios from 'axios';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    const { mediaId } = req.query;

    if (!mediaId) {
      return res.status(400).json({ error: 'mediaId query parameter is required' });
    }

    try {
      const downloadUrl = `${process.env.WHATSAPP_CLOUD_API_URL}/media/${mediaId}`;
      const response = await axios.get(downloadUrl, {
        headers: {
          Authorization: `Bearer ${process.env.WHATSAPP_CLOUD_API_TOKEN}`,
        },
        responseType: 'arraybuffer', // Expect binary data
      });

      // Option 1: Directly return the file as a buffer
      // If you want to force a download:
      // res.setHeader('Content-Disposition', `attachment; filename="${mediaId}.bin"`);
      res.setHeader('Content-Type', response.headers['content-type']);
      return res.send(response.data);

      // Option 2: Or store it in Azure Blob / local storage, then respond with a success message.
    } catch (error) {
      console.error('Download error:', error?.response?.data || error.message);
      return res.status(500).json({ error: error?.response?.data || error.message });
    }
  } else {
    res.setHeader('Allow', ['GET']);
    return res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
