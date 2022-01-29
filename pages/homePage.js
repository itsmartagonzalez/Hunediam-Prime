const ipcRenderer = require('electron').ipcRenderer
const {runPython} = require('../websitePythonScripts/runPython.js')

const moviesParent = document.getElementsByClassName('movie-container')[0];

let = currentUser = '1';

ipcRenderer.on('store-idUser', (event,store) => {
  currentUser = store
  console.log('current ' + currentUser)
});

const getMovies = (userID) => {
  runPython('./websitePythonScripts/getRatedMovies.py', [userID], createMovieList);
}

const createMovieList = (sendArgs, movieList) => {
  movieList = movieList.replaceAll(`':`, `":`);
  movieList = movieList.replaceAll(`', '`, `", "`);
  movieList = movieList.replaceAll(`{'`, `{"`);
  movieList = movieList.replaceAll(`: '`, `: "`);
  movieList = movieList.replaceAll(`, '`, `, "`);
  movieList = movieList.replaceAll(`'}`, `"}`);
  movieList = JSON.parse(movieList);
  movieList['movies'].forEach((movie) => {
    console.log(movie)
    const li = document.createElement("li");
    const img = document.createElement("img");
    const title = document.createElement("h3");
    img.src = movie["image"];
    img.alt = movie["title"] + " poster";
    title.innerHTML = movie["title"];
    li.appendChild(img);
    li.appendChild(title);
    moviesParent.appendChild(li);
  })

}


getMovies(currentUser);
/*for (let i = 1; i < 611; i++) {
  getMovies(moviesParent, i);
}*/