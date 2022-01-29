// const runPython = (program, arguments, callback) => {
//   let programToRun = [program, ...arguments];
//   const python = require('child_process').spawn('python', programToRun);
//   python.stdout.on('data',function(data){
//     //console.log("data: ",data.toString('utf8'));
//     callback(data.toString('utf8'));
//   });
// }
//
// const infoPrint = (info) => {
//   console.log(info);
// }

process.env['ELECTRON_DISABLE_SECURITY_WARNINGS']=true

// Modules to control application life and create native browser window
const {app, BrowserWindow, ipcMain} = require('electron')
const path = require('path')
const url = require('url')

let mainWindow = {}

function createWindow () {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: true,
      contextIsolation: false
    }
  })
  mainWindow.maximize()
  // and load the index.html of the app.
  mainWindow.loadFile('./pages/recommendationPage.html')

  //runPython('./getMovieData.py', ['1', '2'], infoPrint);

  // Open the DevTools.
  // mainWindow.webContents.openDevTools()
}

ipcMain.on('change-home', (event, data)=> {
  BrowserWindow.getAllWindows()[0].loadURL(url.format({
    pathname : path.join(__dirname,'/pages/homePage.html'),
    protocol:'file',
    slashes:true
  }))
  
  BrowserWindow.getAllWindows()[0].webContents.on('did-finish-load', () => {
    BrowserWindow.getAllWindows()[0].webContents.send('store-idUser', data);
  })
  //currentUser = data[0]
  //console.log(currentUser)
})

ipcMain.on('change-recommendation', (event, data)=> {
  BrowserWindow.getAllWindows()[0].loadURL(url.format({
    pathname : path.join(__dirname,'/pages/recommendationPage.html'),
    protocol:'file',
    slashes:true
  }))
  
  BrowserWindow.getAllWindows()[0].webContents.on('did-finish-load', () => {
    BrowserWindow.getAllWindows()[0].webContents.send('store-idUser-toRecommendation', data);
  })
})

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  createWindow()

  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.

exports.mainWindow = mainWindow;
exports.app = app;