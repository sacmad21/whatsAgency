import { Server } from 'socket.io';

let io;

export default function handler(req, res) {
  if (!io) {
    io = new Server(res.socket.server, {
      path: '/api/socket',
      cors: {
        origin: '*',
      },
    });

    io.on('connection', (socket) => {
      console.log('A user connected');

      // Example: Emit a test event
      socket.emit('test', { message: 'WebSocket is working!' });

      socket.on('disconnect', () => {
        console.log('A user disconnected');
      });
    });
  }

  res.end();
}
