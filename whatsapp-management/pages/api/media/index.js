import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export default async function handler(req, res) {
  const { method } = req;

  switch (method) {
    case 'GET':
      // Retrieve all media records
      try {
        const mediaList = await prisma.media.findMany();
        return res.status(200).json(mediaList);
      } catch (error) {
        return res.status(500).json({ error: error.message });
      }

    case 'POST':
      // Create a new media record
      try {
        const { mediaId, type, url, fileName, size, status } = req.body;

        const newMedia = await prisma.media.create({
          data: {
            mediaId,
            type,
            url,
            fileName,
            size,
            status,
          },
        });
        return res.status(201).json(newMedia);
      } catch (error) {
        console.log(error.stack);
        return res.status(500).json({ error: error.message });
      }

    default:
      res.setHeader('Allow', ['GET', 'POST']);
      return res.status(405).end(`Method ${method} Not Allowed`);
  }
}
