const path = require('path')

const zeroCallback = () => {}

const runPython = (program, originalArgs, callback = zeroCallback) => {
  let programToRun = [program, ...originalArgs];
  console.log(`Running ` + programToRun + ' in path ' + path.join(process.cwd(),));
  const python = require('child_process').spawn('python3',  programToRun);

  let result = "";
  python.stdout.on('data',function(data) {
    result += data.toString('utf8');
  });

  python.on('exit',function() {
    callback(originalArgs, result);
  });

}

module.exports.runPython = runPython;