const ipcRenderer = require('electron').ipcRenderer
const {runPython} = require('./websitePythonScripts/runPython.js')

const textInput = document.getElementById('user-id-input')
const loginButton = document.getElementById('login-button')
const signUpButton = document.getElementById('signup-button')

const checkUser = (sendArgs, userExists) => {
  if (userExists) {
    console.log("User id not found")
    textInput.value = '';
    textInput.placeholder = " Wrong ID. Try again.";
    textInput.classList.add("red");
  } else {
    ipcRenderer.send('change-home', sendArgs[1]);
  }
}

const newUser = (sendArgs, id) => {
  ipcRenderer.send('change-home', id);
}


const getTextInput = () => {
  runPython('./websitePythonScripts/checkUserID.py', [textInput.value], checkUser);
}

const createNewUser = () => {
  runPython('./websitePythonScripts/newUserID.py', [], newUser);
}

if (loginButton) {
  loginButton.addEventListener('click', () => getTextInput())
}

if (signUpButton) {
  signUpButton.addEventListener('click', () => createNewUser())
}

