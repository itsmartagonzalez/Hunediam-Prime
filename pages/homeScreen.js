const ipcRenderer = require('electron').ipcRenderer

currentUser = '';


ipcRenderer.on('store-idUser', (event,store) => {
  currentUser = store
  console.log('current ' + currentUser)
});





console.log(currentUser);


const a = document.querySelector('a')

a.innerHTML = currentUser