const bingo_boxes = document.querySelectorAll('.box');
let start_timer = null;
const jsConfetti = new JSConfetti();

function confettiFY() {
  jsConfetti.addConfetti();
}


// Alla vinnande kombinationer
const winning_combinations = [
  [0, 1, 2, 3, 4],
  [5, 6, 7, 8, 9],
  [10, 11, 12, 13, 14],
  [15, 16, 17, 18, 19],
  [20, 21, 22, 23, 24],
  [0, 5, 10, 15, 20],
  [1, 6, 11, 16, 21],
  [2, 7, 12, 17, 22],
  [3, 8, 13, 18, 23],
  [4, 9, 14, 19, 24],
  [0, 6, 12, 18, 24],
  [4, 8, 12, 16, 20]
];

//Shufflefunktion

var shuffleCounter = 0;

function shuffleChallenges() {
 if (shuffleCounter < 3 ){
  var boxes = document.querySelectorAll('.box');
  var challenges = [];

  boxes.forEach(function(box) {
    var challenge = box.querySelector('.front');
    challenges.push(challenge.textContent);
  });

  challenges.sort(function() {
    return 0.5 - Math.random();
  });

  boxes.forEach(function(box, index) {
    var challenge = box.querySelector('.front');
    if (!box.classList.contains('frozen')) { 
      challenge.textContent = challenges[index];
    }
  });
  shuffleCounter++; 
  }
}



var shuffleButton = document.getElementById('shuffle_button');
shuffleButton.addEventListener('click', shuffleChallenges);

let isTimerEnded = false; //för att kontrollera om timern har slutat
let completedRows = [];
// Detta är en funktion som kollar gör att det möjligt att bara klicka i bingorutor när timern är startad
function box_check() {
  if (start_timer && !isTimerEnded) {
    if (this.classList.contains('green')) {
      this.classList.remove('green');
    } else {
      this.classList.add('green');
    }
    game_win(); // anropar funktionen som säger bingo när man har fem i rad
  }
}

bingo_boxes.forEach(bingo_box => {
  bingo_box.addEventListener('click', box_check);
});

var start = document.getElementById("start");

// Sätter värdena för hour, min, sec beroende på vad som finns i elementen med respektive ID
var hour = document.getElementById("hour");
var min = document.getElementById("minute");
var sec = document.getElementById("second");

// Funktion som gör så att timern räknar ner
function timer() {
  // Om timern är på noll avbryts intervallen och timern slutar räkna ner
  if (hour.value == 0 && min.value == 0 && sec.value == 0) {
    clearInterval(start_timer);
    isTimerEnded = true;
    freeze();
    hour.value = 0;
    min.value = 0;
    sec.value = 0;

  // Är sekunderna över 0 minskas det med 1  
  } else if (sec.value > 0) {
    sec.value--;

  // Är sekunderna 0 och minuterna över 0 sätts sekunderna till 59 och minskar minuterna med 1
  } else if (sec.value == 0 && min.value > 0) {
    sec.value = 59;
    min.value--;

  //Om timmarna är över 0 och minuterna är 0 sätts sekunder och minuter till 59 och timmar minskar med 1
  } else if (hour.value > 0 && min.value == 0) {
    sec.value = 59;
    min.value = 59;
    hour.value--;
}

// shufflefunktion
var preBoxes = document.querySelectorAll('.pre_box');
var preBoxArray = [];

for (var i = 0; i < preBoxes.length; i++) {
  preBoxArray.push(preBoxes[i]);
}

function shuffle(array) {
  var currentIndex = array.length;
  var temporaryValue;
  var randomIndex;

  while (currentIndex !== 0) {
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }
}

var shuffleButton = document.getElementById('shuffle_button');
shuffleButton.addEventListener('click', function() {
  shuffle(preBoxArray);

  var preBingoCard = document.querySelector('.pre_bingo_card');
  preBingoCard.innerHTML = '';

  for (var i = 0; i < preBoxArray.length; i++) {
    preBingoCard.appendChild(preBoxArray[i]);
  }
});


// funktion som skickar förlustmeddelandet
function game_loss() {
  if (hour.value == 0 && min.value == 0 && sec.value == 0) {
    const lossMessage = document.getElementById("loss_message");
    const lossmodalContainer = document.getElementById("loss_modal_container");

    lossMessage.textContent = "GAME OVER";
    lossmodalContainer.style.display = "block";

    freeze();
  }
  
document.getElementById("close_loss_modal").addEventListener("click", function() {
  const lossmodalContainer = document.getElementById("loss_modal_container");
  lossmodalContainer.style.display = "none"; // Göm modalen
});
}


function start_game() {
  // Sätter intervallet på timern så timer funktionen körs varje sekund
  start_timer = setInterval(function() {
    timer();
    game_loss();
  }, 1000);
}

start.addEventListener("click", function() {
  console.log("Startar spelet")
  start_game();

  //Låser input på timme, minut och sekund när användaren tryckt på starta spel
  start.disabled = true;
  hour.disabled = true;
  min.disabled = true;
  sec.disabled = true;
});


document.addEventListener("DOMContentLoaded", function() {
  start_game();
})
document.addEventListener("DOMContentLoaded", function () {
  start_game()

});


// Funktion som kollar om en vinnande kombination har gjorts
function game_win() {
  winning_combinations.forEach((combination) => {
    const greenCount = combination.filter(num => bingo_boxes[num].classList.contains('green')).length;
    if (greenCount === 5 && !completedRows.includes(combination)) {
      completedRows.push(combination);

      const bingo_win = document.getElementById('bingo_win');
      bingo_win.id = 'Show_win';

      const displayTime = 3000;

      setTimeout(() => {
        bingo_win.id = 'bingo_win';
      }, displayTime);

      clearInterval(start_timer);

      freeze();


      confettiFY();
    }
  });
}

// funktion som tar bort eventlistener så att det inte längre går att klicka
function freeze() {
  bingo_boxes.forEach(bingo_box => {
    bingo_box.removeEventListener('click', box_check);
  });
}

function showCharacterCount(input, characterCountId) {
  //Hämtar max antal tecken från input-elementet
  const maxLength = input.maxLength;

  //Hämtar aktuellt antal tecken som matats in
  const currentLength = input.value.length;

  //Räknar hur många tecken som återstår
  const remaining = maxLength - currentLength;

  //Hämtar elementet som visar hur många tecken som återstår
  const characterCountElement = document.getElementById(characterCountId);

  //Uppdaterar characterCount med antalet återstående tecken och gör de till en sträng
  characterCountElement.textContent = remaining.toString();
}

//funktion för modal
function showModal() {
  var modal = document.getElementById("infoModal");
  modal.classList.add("show");
  modal.style.display = "block";
}

function hideModal() {
  var modal = document.getElementById("infoModal");
  modal.classList.remove("show");
  modal.style.display = "none";
}
}
