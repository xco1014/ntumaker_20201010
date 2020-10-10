const CONFIG = require('./config.json');
const path = require('path');
const fs = require('fs');
const io = require('socket.io-client');

const log = function (...args) {
  console.log(`[${(new Date()).toLocaleTimeString()}]`, ...args);
}
  
//Connect to socket
const streamlabs = io(`https://sockets.streamlabs.com?token=${CONFIG.SOCKET_API_TOKEN}`, {transports: ['websocket']});
const logFolderPath = path.resolve('./logs');
const logFilePath = path.join(logFolderPath, `${Date.now()}.log`)

log(`Logging to ${logFilePath}`);

//Perform Action on event
streamlabs.on('event', (eventData) => {
  log(`Event received`, eventData);

  if (!fs.existsSync(logFolderPath)) {
    fs.mkdirSync(logFolderPath);
  }

  fs.appendFileSync(logFilePath, `${JSON.stringify(eventData)}\n`, { flag: 'a+' });

  // if (!eventData.for && eventData.type === 'donation') {
  //   //code to handle donation events
  //   log(eventData.message);
  // }
  // if (eventData.for === 'twitch_account') {
  //   switch(eventData.type) {
  //     case 'follow':
  //       //code to handle follow events
  //       log(eventData.message);
  //       break;
  //     case 'subscription':
  //       //code to handle subscription events
  //       log(eventData.message);
  //       break;
  //     default:
  //       //default case
  //       log(eventData.message);
  //   }
  // }
});