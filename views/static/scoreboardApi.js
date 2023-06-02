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
  
  const API_URL = getCookie("API_URL");
  let username = prompt_username();
  let id = generate_id();
  let score = 0;
  let checkedNumbers = [];
  
  async function update_scoreboard() {
    const response = await fetch(`${API_URL}?score=true&id=${id}&name=${username}&points=${score}`);
    const jsonData = await response.json();
    console.log(jsonData);
  }
  
  function prompt_username() {
    const username = prompt("Ditt namn tack?");
    return username;
  }
  
  function generate_id() {
    const id = Math.floor(Math.random() * 100000) + 1;
    return id;
  }
  
  function updateScore(number) {
    if (!checkedNumbers.includes(number)) {
      checkedNumbers.push(number);
      score++;
      update_scoreboard();
    }
  }
  
  
  function game_win() {
    winning_combinations.forEach((combination) => {
      const greenCount = combination.filter(num => bingo_boxes[num].classList.contains('green')).length;
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
  }
  