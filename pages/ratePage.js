const ipcRenderer = require('electron').ipcRenderer
const {runPython} = require('../websitePythonScripts/runPython.js')

const header = document.getElementsByClassName('header')[0]
const searchButton = document.getElementById('search-button');
const parentMovies = document.getElementsByClassName('movie-display')[0];

let currentUser = '1';

ipcRenderer.on('store-idUser-toRate', (event,store) => {
  currentUser = store
  console.log('current ' + currentUser)
});

function autocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  let currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {
      let a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("div");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(val.length);
          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          /*execute a function when someone clicks on the item value (DIV element):*/
          b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
          });
          a.appendChild(b);
        }
      }
      console.log(a)
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      let x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (let i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    let x = document.getElementsByClassName("autocomplete-items");
    for (let i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
    closeAllLists(e.target);
  });
}

let movies = [];
 
const getMovieTitles = (sendArgs, movieTitles) => {
  //console.log(mo)
 console.log(movieTitles.substring(0, 20));
 movies = JSON.parse(movieTitles)['Titles'];
  autocomplete(document.getElementById("movieInput"), movies);
}

const getMovie = (movieTitle) => {
  console.log(movieTitle);
  if (movieTitle) {
    runPython('./websitePythonScripts/getMovieData.py', [movieTitle], showMovie);
  }
}

const showMovie = (sendArgs, movieData) => {
  if (movieData.length > 10) {
    parentMovies.innerHTML = "";
    movieData = JSON.parse(movieData)
    console.log(movieData)
    const titleAndOverview = document.createElement('div');
    const title = document.createElement('h2');
    const overview = document.createElement('p');
    const img = document.createElement('img');
    titleAndOverview.classList.add("title-overview");
    overview.textContent = movieData["overview"];
    img.src = movieData["image"];
    img.alt = movieData["title"] + " poster";
    title.textContent = movieData["title"];
    parentMovies.appendChild(img);
    titleAndOverview.appendChild(title);
    titleAndOverview.appendChild(overview);
    parentMovies.appendChild(titleAndOverview);
    addStars(titleAndOverview);
    const ratingStars = [...document.getElementsByClassName("rating__star")];
    executeRating(ratingStars, movieData["id"]);
  }
}

const addStars = (parent) => {
  const rating = document.createElement('div');
  rating.classList.add("rating");
  for (let i = 0; i < 5; i++) {
    const star = document.createElement('i');
    star.classList.add("rating__star", "fa","fa-star");

    rating.appendChild(star);
  }
  const h3 = document.createElement('h3');
  h3.textContent = "Please, rate this movie!"
  rating.appendChild(h3);
  parent.appendChild(rating);
}

function executeRating(stars, movieID) {
  const starClassActive = "rating__star fa fa-star checked";
  const starClassInactive = "rating__star fa fa-star";
  const starsLength = stars.length;
  let i;
  stars.map((star) => {
    star.onclick = () => {
      i = stars.indexOf(star);
      let newRating;
      if (star.className===starClassInactive) {       
        newRating = stars.indexOf(star) + 1;
        for (i; i >= 0; --i) stars[i].className = starClassActive;
      } else {
        newRating = stars.indexOf(star);
        for (i; i < starsLength; ++i) stars[i].className = starClassInactive;
      }
      document.getElementsByClassName('rating')[0].querySelector('h3').textContent = "Thanks for rating this movie."
      console.log("New Rating: " + newRating);
      runPython('./websitePythonScripts/setNewRating.py', [currentUser, movieID, newRating]);
    };
 });
}
 
runPython('./websitePythonScripts/getAllMovies.py', [], getMovieTitles);

if (header) {
  header.addEventListener('click', () => changeToHomePage())
}

const textInput = document.getElementById('movieInput');

if (searchButton) {
  searchButton.addEventListener('click', () => getMovie(textInput.value))
}

const changeToHomePage = () => {
  ipcRenderer.send('change-home', currentUser);
}



