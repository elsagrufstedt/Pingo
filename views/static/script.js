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

const starting_minutes=10;
let time = starting_minutes * 60;

const countdown_el = document.getElementById('countdown');

setInterval(update_countdown, 1000)

function update_countdown(){
  const minutes = Math.floor(time/60);
  let seconds = time % 60;

  seconds = seconds < 10 ? '0' + seconds : seconds;

  countdown_el.innerHTML = `${minutes}: ${seconds}`;
  time--;
}