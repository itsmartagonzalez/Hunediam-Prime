const ipcRenderer = require('electron').ipcRenderer
const {runPython} = require('../websitePythonScripts/runPython.js')

const header = document.getElementsByClassName('header')[0]
const moviesParent = document.getElementsByClassName('movie-container')[0];
let currentUser = '1';
let movieList = {}

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

const checkAmountOfMovies = (sendArgs, moviesAmount) => {
  movieCounter = moviesAmount.slice(2, -4);
  console.log("Movies Amount: " + movieCounter);
  let title = document.createElement("h2");
  let content = document.getElementsByClassName("content-text")[0];
  let movieContainer = document.getElementsByClassName("movie-container")[0];
  if (movieCounter < 5) {
    let rateButton = document.createElement("button");
    let h2 = document.createElement("h2");
    title.innerHTML = `You have rated ${movieCounter} movies.
                        Try rating at least 5 to receive personalized recommendations.`;
    content.appendChild(title);
    rateButton.innerHTML = "Rate more Movies";
    rateButton.id = "rate-button";
    content.appendChild(rateButton);
    h2.innerHTML = "Nevertheless, here you have the best rated movies of all time.";
    content.appendChild(h2);
    // Imprimir que tiene pocas rated movies 
    // poner boton para rate movies
    // show best rated movies
    runPython('./websitePythonScripts/getBestRatedMovies.py', [], createMovieList);
  } else {
    title.innerHTML = "Movies you might like...";
    content.appendChild(title);
    // make recomendation
    // show recommended movies
  }
}

const getRecommendedMovies = (userID) => {
  runPython('./websitePythonScripts/getAmountOfRatedMovies.py', [userID], checkAmountOfMovies);
}

if (header) {
  header.addEventListener('click', () => changeToHomePage())
}

const changeToHomePage = () => {
  ipcRenderer.send('change-home', currentUser);
}

ipcRenderer.on('store-idUser-toRecommendation', (event,store) => {
  currentUser = store
  console.log('current ' + currentUser)
  getRecommendedMovies(currentUser)
});
