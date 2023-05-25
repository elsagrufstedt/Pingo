const bingo_boxes = document.querySelectorAll('.box');

let isTimerEnded = false; //för att kontrollera om timern har slutat

bingo_boxes.forEach(bingo_box => {
  bingo_box.addEventListener('click', box_check);
  //Detta är en funktion som kollar gör att det möjligt att bara klicka i bingorutor när timern är startad
  function box_check() {
    if (start_timer && !isTimerEnded) {
      if (this.classList.contains('green')) {
        this.classList.remove('green');
      } else {
        this.classList.add('green');
      }
      game_win(); //anropar funktionen som säger bingo när man har fem i rad
    }
  };
});

var start_timer = null;

var start = document.getElementById("start");

var hour = document.getElementById("hour");
var min = document.getElementById("minute");
var sec = document.getElementById("second");

function timer() {
  if (hour.value == 0 && min.value == 0 && sec.value == 0) {
    clearInterval(start_timer);
    isTimerEnded = true;
    freeze();
  } else if (sec.value != 0) {
    sec.value--;
  } else if (sec.value == 0 && min.value != 0) {
    sec.value = 59;
    min.value--;
  } else if (hour.value != 0 && min.value == 0) {
    min.value = 59;
    hour.value--;
  }
}

//funktion som skickar förlustmeddelandet
function game_loss() {
  if (hour.value == 0 && min.value == 0 && sec.value == 0) {
    const lossMessage = document.getElementById("loss_message");
    const lossmodalContainer = document.getElementById("loss_modal_container");
    
    lossMessage.textContent = "Åhnej! Tiden tog slut, du har förlorat.";
    lossmodalContainer.style.display = "block"

    freeze();
  }
}

document.getElementById("close_loss_modal").addEventListener("click", function () {
  const lossmodalContainer = document.getElementById("loss_modal_container");
  lossmodalContainer.style.display = "none"; // Göm modalen
});


function start_game() {
  start_timer = setInterval(function () {
    timer();
    game_loss();
  }, 1000);
}

start.addEventListener("click", function () {
  console.log("Startar spelet");
  start_game();
  start.disabled = true;
  document.getElementById("hour").disabled = true;
  document.getElementById("minute").disabled = true;
  document.getElementById("second").disabled = true;
});

// All vinnande kombinationer
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

// Funktion som kollar om en vinnande kombination har gjorts
let completedRows = [];

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
    }
  });
}

//funktion som tar bort eventlistener så att det inte längre går att klicka
function freeze() {
  bingo_boxes.forEach(bingo_box => {
    bingo_box.removeEventListener('click', box_check);
  });
}
