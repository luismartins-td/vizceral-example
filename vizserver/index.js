var http = require('http').createServer();
var io = require('socket.io')(http);

http.listen(5000, () => {
  console.log('listening on *:5000');
});

io.on('connection', (socket) => {
  console.log('a user connected');
  socket.emit('connected');

  socket.on('disconnect', () => {
    console.log('user disconnected');
  });

  socket.on('ping', (data) => {
    console.log("Received PING:" + data);
    socket.emit('PONG', 'pong data');
  });

  socket.on('freshData', (data) => {
    console.log(JSON.stringify(data));
    socket.broadcast.emit('freshData', data);
  });

});

// setInterval(() => {
//   console.log('Sending new Data...');
//   io.emit('pong', Date.now());
// },5000);
