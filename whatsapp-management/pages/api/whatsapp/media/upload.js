// pages/api/whatsapp/media/upload.js
import axios from 'axios';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    try {
      /**
       * Expected body params:
       * - file: The file (binary data or base64).
       * - mimeType: e.g. "image/jpeg", "video/mp4", etc.
       * 
       * Alternatively, you might accept a URL or a form-data upload.
       * This example is simplified. Adjust as needed.
       */

      const { file, mimeType } = req.body;

      // If your data is base64-encoded, you'd need to convert it to a buffer.
      // For demonstration, we’ll assume it’s already a Buffer or base64 string.
      const uploadUrl = `${process.env.WHATSAPP_CLOUD_API_URL}/media`;

      const formData = new FormData();
      const blob = new Blob([file], { type: mimeType });
      formData.append('file', blob);
      formData.append('messaging_product', 'whatsapp'); // Required by Meta

      // Send to WhatsApp
      const response = await axios.post(uploadUrl, formData, {
        headers: {
          Authorization: `Bearer ${process.env.WHATSAPP_CLOUD_API_TOKEN}`,
          ...formData.getHeaders?.()
        },
      });

      // e.g. response.data => { "id": "MEDIA_ID_FROM_WHATSAPP" }
      return res.status(200).json(response.data);
    } catch (error) {
      console.error('Upload error:', error?.response?.data || error.message);
      return res.status(500).json({ error: error?.response?.data || error.message });
    }
  } else {
    res.setHeader('Allow', ['POST']);
    return res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
