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

const createMovieLiElement = (movie) => {
  let li = document.createElement("li");
  let flipCard = document.createElement("div");
  flipCard.classList.add("flip-card");
  let flipCardInner = document.createElement("div");
  flipCardInner.classList.add("flip-card-inner");
  let flipCardFront = document.createElement("div");
  flipCardFront.classList.add("flip-card-front");
  let flipCardBack = document.createElement("div");
  flipCardBack.classList.add("flip-card-back");
  const img = document.createElement("img");
  const title = document.createElement("h3");
  const overview = document.createElement("p");
  overview.textContent = movie["overview"];
  img.src = movie["image"];
  img.alt = movie["title"] + " poster";
  title.textContent = movie["title"];
  flipCard.appendChild(flipCardInner);
  flipCardInner.appendChild(flipCardFront);
  flipCardFront.appendChild(img);
  flipCardInner.appendChild(flipCardBack);
  flipCardBack.appendChild(title);
  flipCardBack.appendChild(overview);
  li.appendChild(flipCard);
  moviesParent.appendChild(li);
}

const createMovieList = (sendArgs, movieLista) => {
  movieList = JSON.parse(movieLista);
  movieList['movies'].forEach((movie) => {
    //console.log(movie)
    createMovieLiElement(movie);
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
