// /pages/api/phoneNumber/index.js

import { PrismaClient } from '@prisma/client';
const prisma = new PrismaClient();

export default async function handler(req, res) {
  try 
  {
    if (req.method === 'GET') {
      const phoneNumbers = await prisma.phoneNumber.findMany();
      console.log("Get all Numbers");
      console.log(phoneNumbers);
      return res.status(200).json(phoneNumbers);
    }

    if (req.method === 'POST') {
      const { phoneNumber, status, twoStepVerificationStatus } = req.body;
            
      const newPhoneNumber = await prisma.phoneNumber.create({
        data: {
          phoneNumber,
          status,
          twoStepVerificationStatus
        },
      });
      return res.status(201).json(newPhoneNumber);
    }

    return res.status(405).send('Method Not Allowed');
  } catch (error) {
    console.log("ERROR-----");
    console.error(error);
    return res.status(500).json({ error: error.message });
  }
}
