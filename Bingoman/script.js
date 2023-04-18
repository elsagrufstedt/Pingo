async function categories() {

  const requestURL = './categories.json';
  const request = new Request(requestURL);
  const response = await fetch(request);
  const result = await response.json();
  console.log(result)

  pingo_game(result)
}

/* Funktion som väljer .board klassen och därefter kör en for-loop som itererar igenom hela "challenges" listan
 för varje utmaning i listan skapas en ny div med klass-namnet "square" som senare får husa texten av de indexet som loopen var på
 Efter loopen görs en event-listener som vid en klick på square elementet byter klassen från "square" till "won". Till sist appendar vi dem nya 
 div elementen till "board" containern. 
*/

function pingo_game(result) {
const challenges = result[0].challenges;
const board = document.querySelector(".board");
for (let i = 0; i < challenges.length; i++) {
  const square = document.createElement("div");
  square.classList.add("square");
  square.textContent = challenges[i];
  square.addEventListener("click", function () {
    this.classList.toggle("won");
  });
  board.appendChild(square);
}
}


categories();