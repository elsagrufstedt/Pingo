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
