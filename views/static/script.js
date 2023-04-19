function pingo_game() {
  const square = document.querySelector(".box");
  square.addEventListener("click", function () {
      this.classList.toggle("won");
    });
  }

pingo_game();
