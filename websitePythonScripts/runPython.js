const path = require('path')

const zeroCallback = () => {}

const runPython = (program, arguments, callback = zeroCallback) => {
  let programToRun = [program, ...arguments];
  console.log(`Running ` + programToRun + ' in path ' + path.join(process.cwd(),));
  const python = require('child_process').spawn('python',  programToRun);

  let result = "";
  python.stdout.on('data',function(data) {
    result += data.toString('utf8');
  });

  python.on('exit',function() {
    callback(arguments, result);
  });

}

module.exports.runPython = runPython;