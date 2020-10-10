const { SOCKET_API_TOKEN } = require('./config.json');
const path = require('path');
const fs = require('fs');
const io = require('socket.io-client');
const { runPython } = require('./pythonHelper');
const TaskQueue = require('./TaskQueue');

const { log, debug, error } = require('./logging')('streamlabs');

function subscribe() {
  const streamlabs = io(`https://sockets.streamlabs.com?token=${SOCKET_API_TOKEN}`, { transports: ['websocket'] });
  log(`subscribed to streamlabs`);

  const logFolderPath = path.resolve('logs');
  const logFilePath = path.join(logFolderPath, `${Date.now()}.log`);
  log(`Logging events to '${logFilePath}'`);

  const taskQueue = new TaskQueue();

  streamlabs.on('event', async (e) => {
    try {
      log(`Event received`, e);

      if (!fs.existsSync(logFolderPath)) {
        fs.mkdirSync(logFolderPath);
      }

      fs.appendFileSync(logFilePath, `${JSON.stringify(e)}\n`, { flag: 'a+' });

      if (e.type === 'bits' && e.for === 'twitch_account') {
        await doWatering(e.message[0].amount);
      }

      if (e.type === 'donation') {
        await doWatering(e.message[0].amount);
      }
    }
    catch (err) {
      error('Error executing cb.', err);
    }
  });

  async function doWatering(amount) {
    await taskQueue.enqueue(async () => {
      await runPython('main.py', amount);
    });
  }
}


module.exports = subscribe
