const Verbose = require('./config.json').Verbose;

function getTimeTag() {
  return `[${(new Date()).toLocaleTimeString()}]`;
}

module.exports = function (tag) {
  tag = `[${tag}]`;
  return {
    log(...args) {
      console.log(getTimeTag(), tag, '[info]', ...args);
    },
    debug(...args) {
      Verbose && console.log(getTimeTag(), tag, '[debug]', ...args);
    },
    error(...args) {
      console.error(getTimeTag(), tag, '[error]', ...args);
    }
  }
}
