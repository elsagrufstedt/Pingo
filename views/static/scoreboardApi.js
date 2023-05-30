function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
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

async function update_scoreboard(id, name, score) {
    const response = await fetch(API_URL + `?score=true&id=${id}&name=${name}&points=${score}`);    
    const jsonData = await response.json();
    console.log(jsonData);
}

/*
    // Testing the script
    update_scoreboard(1, "Kalle", 0);
*/