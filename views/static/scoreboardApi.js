function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

const API_URL = "https://antontibblin.se/alumnmiddag/api.php";
let username = prompt_username();
let id = generate_id();
let score = 0;
let checkedNumbers = [];

async function update_scoreboard() {
  const response = await fetch(`${API_URL}?score=true&id=${id}&name=${username}&points=${score}`);
  const jsonData = await response.json();
  console.log(jsonData);
}
update_scoreboard(); // Update scoreboard when page is loaded

function prompt_username() {
  const username = prompt("Ditt namn tack?");
  return username;
}

function generate_id() {
  const id = Math.floor(Math.random() * 100000) + 1;
  return id;
}

function updateScore(number) {
  /*
  if (!checkedNumbers.includes(number)) {
    checkedNumbers.push(number);
    score++;
    update_scoreboard();
  }
  */
}


function game_win() {
  let current_points = 0;
  winning_combinations.forEach((combination) => {
    const greenCount = combination.filter(num => bingo_boxes[num].classList.contains('green')).length;

    // Calculate how many points the user have
    let p = 0;
    for (let i = 0; i < winning_combinations.length; i++) {
      const correctNumbers = combination.filter(num => bingo_boxes[num].classList.contains('green'));
      if (correctNumbers.length > p) {
        p = correctNumbers.length;
      }
    }
    if (p > current_points) {
      current_points = p;  
    }

    

    if (greenCount === 5 && !completedRows.includes(combination)) {
      completedRows.push(combination);
      
      const correctNumbers = combination.filter(num => bingo_boxes[num].classList.contains('green'));
      correctNumbers.forEach(num => updateScore(num));
      
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

  score = current_points;
  update_scoreboard();
}
