const subscribe = require('./streamlabs');
const { log, debug, error } = require('./logging')('Main');

async function activate() {
  try {
    subscribe();
  }
  catch (err) {
    error(err);
  }
}

activate();