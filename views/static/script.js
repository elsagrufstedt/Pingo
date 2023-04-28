const bingo_boxes = document.querySelectorAll('.box');

// Kodrad som räknar 
bingo_boxes.forEach(bingo_box => {
  bingo_box.addEventListener('click', function() {
    if (this.classList.contains('green')) {
      this.classList.remove('green');
    } else {
      this.classList.add('green');
    }
    game_win();
  });
});

var start_timer = null;

var start = document.getElementById("start");
var reset = document.getElementById("reset");

var hour = document.getElementById("hour");
var min = document.getElementById("minute");
var sec = document.getElementById("second");

function timer(){
  if(hour.value == 0 && min.value == 0 && sec.value == 0){
    hour.value = 0;
    min.value = 0;
    sec.value = 0;
  } else if(sec.value != 0){
    sec.value --;
  } else if(min.value != 0 && sec.value == 0){
    sec.value = 59;
    min.value --;
  } else if(hour.value != 0 && min.value == 0){
    min.value = 60;
    hour.value --;
  }
  return
}

start.addEventListener("click", function(){
  function start_game(){
    start_timer = setInterval(function(){
      timer();
    }, 1000)
  }
  start_game()
  start.disabled = true;
  document.getElementById("hour").disabled = true;
  document.getElementById("minute").disabled = true;
  document.getElementById("second").disabled = true;
})

//Alla vinnande kombinationer
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


//Funktion som kollar om en vinnande kombination har gjorts
function game_win() {
  winning_combinations.forEach((combination) => {
    const greenCount = combination.filter(num => bingo_boxes[num].classList.contains('green')).length;
    if (greenCount === 5) { //Kollar om alla fem boxar i en vinnande kombination är klickade
      const bingo_win = document.getElementById('bingo_win');
      bingo_win.setAttribute('id', 'Show_win');//Visar BINGO!- elementet

      bingo_boxes.forEach(bingo_box => {
        bingo_box.removeEventListener('click', game_win); //(inte färdig)Gör det omöjligt att klicka i fler rutor
      });
    }
  });
}

