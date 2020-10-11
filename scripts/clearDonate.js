async function clear() {
  let donate;
  while(donate = document.querySelector('.pane-dropdown__link.warn')) {
    document.querySelector('.pane-dropdown__link.warn').click();
    await sleep(100);
    document.getElementById('button-1').click();
    await sleep(1000);
  }
}

async function sleep(ms = 1000) {
  return new Promise(r => setTimeout(r, ms));
}

clear()