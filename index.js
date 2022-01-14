const {PythonShell} = require('python-shell')
const path = require("path")


const runPython = (program, arguments, callback) => {

  let options = {
    scriptPath : path.join(__dirname, '/'),
    args : arguments
  }

  let pyshell = new PythonShell(program, options);


  pyshell.on('message', function(message) {
    callback(message);
  });
  // document.getElementById("city").value = "";
  // let programToRun = [program, ...arguments];
  // const python = require('child_process').spawn('python', programToRun);
  // python.stdout.on('data',function(data){
  //   //console.log("data: ",data.toString('utf8'));
  //   callback(data.toString('utf8'));
  // });
}

const infoPrint = (info) => {
  console.log(info);
  alert(info);
}

runPython('./getMovieData.py', ['1', '2'], infoPrint);