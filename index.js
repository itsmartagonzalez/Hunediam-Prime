const {remote} = require('electron')
const ipcRenderer = require('electron').ipcRenderer

const runPython = (program, arguments, callback) => {
  let programToRun = [program, ...arguments];
  const python = require('child_process').spawn('python', programToRun);
  python.stdout.on('data',function(data){
    //console.log("data: ",data.toString('utf8'));
    callback(data.toString('utf8'));
  });
}

const infoPrint = (info) => {
  console.log(info);
  //alert(info);
}

const textInput = document.getElementById('user-id-input');
const submitButton = document.querySelector('.submit')

const getTextInput = () => {
  console.log(textInput.value);
  // FALTA COMPROBAR EL ID y que no este vacío
  ipcRenderer.send('change-home');
}

submitButton.addEventListener('click', () => getTextInput())

//runPython('./websitePythonScripts/getMovieData.py', ['1', '2'], infoPrint);
