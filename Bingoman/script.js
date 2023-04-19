// En lista på möjliga utmaningar
const challenges = [
    "Drick en öl på 10sek",
    "Ta bild med en ordningsvakt",
    "Hitta någon med samma förnamn",
    "Få en kondom",
    "Vinn i sten, sax, påse",
    "Sjung en snappsvisa med en främling",
    "Dansa macarena med minst 3 främlingar",
    "Övertala någon att ni känner varann",
    "Gör en kullerbytta",
    "Bjud en främling på en drink",
    "Drick ett glas vatten",
    "Bada i en fontän",
    "Ät en hamburagre",
    "Få en tampong",
    "Ta bild med bartendern",
    "Byt Strumpor med en främling",
    "Övertyga en främling att ladda  ner Pingo",
    "Drick en kvarlämnad slatt",
    "Ge en främling en massage",
    "Få bartendern att servera dig en drink du hittat på", 
    "Ta en bodyshot", 
    "Starta ett danståg", 
    "Smit före i en kö",
    "Fånga någon på din fiskelina",
    "Få en främling att skratta"
  ];
  
  /* Väljer .board klassen och för varje utmaning i "challenges" skapas ny div med klass-namnet "square"
     som får texten av de indexet som loopen var på, efter loopen görs en event-listener som vid klick på square 
     byter klass från "square" till "won". Hämtar de nya divsen till "board" containern.
*/

  function pingo_game() {
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
  
  pingo_game()