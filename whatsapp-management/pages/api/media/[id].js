import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export default async function handler(req, res) {
  const {
    method,
    query: { id },
  } = req;

  switch (method) {
    case 'GET':
      try {
        const mediaItem = await prisma.media.findUnique({
          where: { id: parseInt(id) },
        });
        if (!mediaItem) {
          return res.status(404).json({ error: 'Media not found' });
        }
        return res.status(200).json(mediaItem);
      } catch (error) {
        return res.status(500).json({ error: error.message });
      }

    case 'PUT':
      try {
        const { mediaId, type, url, fileName, size, status } = req.body;
        const updatedMedia = await prisma.media.update({
          where: { id: parseInt(id) },
          data: {
            mediaId,
            type,
            url,
            fileName,
            size,
            status,
          },
        });
        return res.status(200).json(updatedMedia);
      } catch (error) {
        return res.status(500).json({ error: error.message });
      }

    case 'DELETE':
      try {
        await prisma.media.delete({
          where: { id: parseInt(id) },
        });
        return res.status(204).end();
      } catch (error) {
        return res.status(500).json({ error: error.message });
      }

    default:
      res.setHeader('Allow', ['GET', 'PUT', 'DELETE']);
      return res.status(405).end(`Method ${method} Not Allowed`);
  }
}
