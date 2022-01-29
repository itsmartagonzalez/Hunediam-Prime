const path = require('path')

const runPython = (program, arguments, callback) => {
  let programToRun = [program, ...arguments];
  console.log(`Running ` + programToRun + ' in path ' + path.join(process.cwd(),));
  const python = require('child_process').spawn('python',  programToRun);
  python.stdout.on('data',function(data) {
    // console.log("data: ",data.toString('utf8'));
    callback(arguments, data.toString('utf8'));
  });
}

module.exports.runPython = runPython;