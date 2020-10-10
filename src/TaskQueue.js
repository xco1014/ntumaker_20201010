module.exports = function () {
  this.queue = [];
  this.enqueue = async function (cb) {
    let resolve, reject;
    const p = new Promise((res, rej) => {
      resolve = res;
      reject = rej;
    })
    this.queue.push({ cb, resolve, reject });
    this.run();
    return p;
  }
  this.run = async function() {
    if (this.running) return;
    this.running = true;
    while(this.queue.length) {
      const task = this.queue.shift();
      try {
        task.resolve(await task.cb());
      }
      catch(err) {
        task.reject(err);
      }
    }
    this.running = false;
  }
}