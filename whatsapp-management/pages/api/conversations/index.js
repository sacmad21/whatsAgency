import prisma from '../../../lib/prisma';

export default async function handler(req, res) {

  if (req.method === 'GET') {
    const conversations = await prisma.conversation.findMany({
      include: { phoneNumber: true },
    });
    res.status(200).json(conversations);
  } 
  else
  if (req.method === 'POST') {
    console.log("Conversation POST body");
    console.log(req.body);
    
    const { phoneNumberId, conversationType } = req.body;
    const conversation = await prisma.conversation.create({
      data: { phoneNumberId, conversationType },
    });
    res.status(201).json(conversation);
  }
  else
  if (req.method === 'PUT') {
    const { id, conversationType } = req.body;
    const conversation = await prisma.conversation.update({
      where: { id },
      data: { conversationType },
    });
    res.status(200).json(conversation);
  }
  else
  if (req.method === 'DELETE') {
    const { id } = req.body;
    await prisma.conversation.delete({ where: { id } });
    res.status(204).end();
  }
  else
    {
    console.log("Method is not available")
    }
  


}
