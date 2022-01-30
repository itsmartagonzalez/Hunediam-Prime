const ipcRenderer = require('electron').ipcRenderer
const { runPython } = require('../websitePythonScripts/runPython.js')

const moviesParent = document.getElementsByClassName('movie-container')[0];
const welcomeElement = document.getElementsByClassName('sidebar')[0].querySelector('h2')
const rateButton = document.getElementById('rate-more-button')
const recommendButton = document.getElementById('recommendations-button')
const header = document.getElementsByClassName('header')[0]
const svdButton = document.getElementById('svd-button')
const contentBasedButton = document.getElementById('content-based-button')

let currentUser;
let movieList = {}

ipcRenderer.on('store-idUser', (event, store) => {
  console.log('usuario ' + store)
  currentUser = parseInt(store)
  welcomeElement.innerHTML = "welcome <br>user " + currentUser;
  getMovies(currentUser);
});

const getMovies = (userID) => {
  runPython('./websitePythonScripts/getRatedMovies.py', [userID], checkAmountOfMovies);
}

const checkAmountOfMovies = (sendArgs, movieLista) =>{
  console.log(movieLista)
  if (movieLista.length > 15) {
    movieList = JSON.parse(movieLista);
    moviesParent.innerHTML = "";
    createMovieList(movieList)
  } else {
    const text = document.getElementsByClassName('movies')[0].querySelector('h2')
    text.innerHTML = " It seems like you have not rated any movies...<br>Try rating at least 5 to receive personalized recommendations.";
    document.getElementsByClassName('movie-container')[0].style.all = 'initial';
  }
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

const createMovieList = (movieList) => {
  movieList['movies'].forEach((movie) => {
    //console.log(movie)
    createMovieLiElement(movie);
  })
}

// if (recommendButton) {
//   recommendButton.addEventListener('click', () => changeToRecommenderPage())
// }

const changeToRecommenderPage = () => {
  header.removeEventListener('click', () => changeToLogin())
  ipcRenderer.send('change-recommendation', currentUser);
}

// if (rateButton) {
//   rateButton.addEventListener('click', () => changeToRatePage())
// }

const changeToRatePage = () => {
  header.removeEventListener('click', () => changeToLogin())
  ipcRenderer.send('change-rate', currentUser);
}

if (header) {
  header.addEventListener('click', () => changeToLogin())
}

const changeToLogin = () => {
  header.removeEventListener('click', () => changeToLogin())
  ipcRenderer.send('change-login', currentUser);
}

const changeSVD = () => {
  header.removeEventListener('click', () => changeToLogin())
  ipcRenderer.send('change-svd', currentUser);
}

// if (svdButton) {
//   svdButton.addEventListener('click', changeSVD())
// }

const changeContentBased = () => {
  header.removeEventListener('click', () => changeToLogin())
  ipcRenderer.send('change-content-based', currentUser);
}

// if (contentBasedButton) {
//   contentBasedButton.addEventListener('click', changeContentBased())
// }