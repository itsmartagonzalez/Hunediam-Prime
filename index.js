
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
  alert(info);
}

runPython('./websitePythonScripts/getMovieData.py', ['1', '2'], infoPrint);
