// /pages/api/phoneNumber/whatsapp/broadcast.js
import { PrismaClient } from '@prisma/client';
import axios from 'axios';

const prisma = new PrismaClient();

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { phoneNumbers, phoneNumbersIds, message } = req.body;

  console.log("Broadcasting numbers :: ", req.body );

  if (!phoneNumbers || phoneNumbers.length === 0) {
    return res.status(400).json({ error: 'No phone numbers provided.' });
  }



  try {
    const results = await Promise.all(
      
      phoneNumbers.map(async (phoneNumber, index) => {
     
     
        console.log("Index:" , index,"\nPhone:", phoneNumber, "\tId:", phoneNumbersIds[index]) ;       
      

      const phoneNumId = phoneNumbersIds[index];

      console.log(phoneNumber, phoneNumId);

        try {
          // 1. Send the message via WhatsApp API
          const response = await axios.post(
            `${process.env.WHATSAPP_API_BASE_URL}/${process.env.WHATSAPP_CLOUD_API_PHONE_NUMBER_ID}/messages`,
            {
              messaging_product: 'whatsapp',
              to: phoneNumber,
              text: { body: message },
            },
            {
              headers: {
                Authorization: `Bearer ${process.env.WHATSAPP_API_TOKEN}`,
                'Content-Type': 'application/json',
              },
            }
          );

          const messageId = response.data.messages[0]?.id || 'unknown';

          const sender =  process.env.WHATSAPP_CLOUD_API_PHONE_NUMBER_ID ;


          // 2. Log the message into the Message table
          await prisma.message.create({
            data: {
              messageId: messageId,
              type: 'TEXT', // Assuming this is a text message
              content: message,
              status: 'SENT',
              direction: 'OUTGOING',
              senderPhoneNumberId: 6,     // If applicable, populate this field with the sender
              recipientPhoneNumberId: phoneNumbersIds[index],  // Map this to the recipient ID from the database
            },
          });

          return { phoneNumber, success: true };
        } catch (error) {
          console.log(error.stack)
          console.error(`Failed to send message to ${phoneNumber}:`, error);
          return { phoneNumber, success: false, error: error.message };
        }

        index = index + 1;

        
      })

  
    );

    const sentCount = results.filter((result) => result.success).length;

    return res.status(200).json({
      success: true,
      sentCount,
      details: results,
    });
  } catch (error) {
    console.log(error.stack);
    return res.status(500).json({
      error: error.response?.data || error.message || 'Unknown error occurred.',
    });
  }
}
