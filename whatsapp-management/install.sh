npm install primereact primereact prisma @prisma/client axios
npm install primeicons  # for PrimeReact icons
npm install --save-dev tailwindcss postcss autoprefixer  # optional, if using Tailwind

npm install @azure/storage-blob
npm install primereact primeicons @emotion/react @emotion/styled
npm install primeflex

ngrok http 3000

npm install socket.io socket.io-client

npx prisma migrate dev --name init

npx prisma generate



#######################################


await prisma.webhooks.create({
  data: {
    event_type: event.type,
    payload: JSON.stringify(event),
    received_at: new Date(),
  },
});



module.exports = {
  async rewrites() {
    return [
      {
        source: '/socket.io/:path*',
        destination: '/api/socket/:path*',
      },
    ];
  },
};
