const ipcRenderer = require('electron').ipcRenderer
const {runPython} = require('./websitePythonScripts/runPython.js')

const checkUser = (sendArgs, id) => {
  if (id == 0) {
    console.log("User id not found")
    // Cambiar CSS para que introduzca ID valido 
  } else {
    ipcRenderer.send('change-home', sendArgs[1]);
  }
}

const textInput = document.getElementById('user-id-input')
const submitButton = document.querySelector('.submit')

const getTextInput = () => {
  console.log(textInput.value);
  // FALTA COMPROBAR EL ID y que no este vacío
  runPython('./websitePythonScripts/checkUserID.py', [textInput.value], checkUser);
}

if (submitButton) {
  submitButton.addEventListener('click', () => getTextInput())
}

