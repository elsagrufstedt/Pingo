const bingo_boxes = document.querySelectorAll('.box');

// Kodrad som räknar 
bingo_boxes.forEach(bingo_box => {
  bingo_box.addEventListener('click', function() {
    if (this.classList.contains('green')) {
      this.classList.remove('green');
    } else {
      this.classList.add('green');
    }
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
})