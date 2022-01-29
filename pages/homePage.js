const ipcRenderer = require('electron').ipcRenderer
const {runPython} = require('../websitePythonScripts/runPython.js')

const moviesParent = document.getElementsByClassName('movie-container')[0];
const welcomeElement = document.getElementsByClassName('sidebar')[0].querySelector('h2')
const rateButton = document.getElementById('rate-more-button')
const recommendButton = document.getElementById('recommendations-button')

let currentUser = '1';

ipcRenderer.on('store-idUser', (event,store) => {
  currentUser = store
});

const getMovies = (userID) => {
  runPython('./websitePythonScripts/getRatedMovies.py', [userID], createMovieList);
}

const createMovieList = (sendArgs, movieLista) => {
  movieList = JSON.parse(movieLista);
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

const changeToRecommenderPage = () => {
  console.log("hola")
  ipcRenderer.send('change-recommendation', currentUser);
}

console.log(recommendButton)
welcomeElement.innerHTML = "welcome <br>user " + currentUser
getMovies(currentUser);

if (recommendButton) {
  recommendButton.addEventListener('click', () => changeToRecommenderPage())
}
