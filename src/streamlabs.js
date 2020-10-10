const { SOCKET_API_TOKEN } = require('./config.json');
const path = require('path');
const fs = require('fs');
const io = require('socket.io-client');

const { log, debug, error } = require('./logging')('streamlabs');

function subscribe() {
  const streamlabs = io(`https://sockets.streamlabs.com?token=${SOCKET_API_TOKEN}`, { transports: ['websocket'] });
  log(`subscribed to streamlabs`);
  
  const logFolderPath = path.resolve('..', 'logs');
  const logFilePath = path.join(logFolderPath, `${Date.now()}.log`);
  log(`Logging events to '${logFilePath}'`);

  streamlabs.on('event', (eventData) => {
    log(`Event received`, eventData);

    if (!fs.existsSync(logFolderPath)) {
      fs.mkdirSync(logFolderPath);
    }

    fs.appendFileSync(logFilePath, `${JSON.stringify(eventData)}\n`, { flag: 'a+' });
  });
}

module.exports = subscribe