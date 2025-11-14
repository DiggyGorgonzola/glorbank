var user_location = 'en-US'
function updateClock() {
    const now = new Date();
    const formattedTime = now.toLocaleTimeString(user_location, {
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
        hour12: false
        });
    const formattedDate = now.toLocaleDateString(user_location, {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
        });

    document.getElementById('clock-display').innerText = `${formattedDate} ${formattedTime}`;

};
function startClock() {
    /*alternative to this line but idk if it'll work:
    
    let clockDisplay = document.createElement("div");
    clockDisplay.id = "clock-display";
    clockDisplay.style.position = "absolute";
    clockDisplay.style.fontSize = "10px";
    clockDisplay.style.textAlign = "left";
    clockDisplay.style.textDecoration = "0px";
    document.body.appendChild(clockDisplay);
    */
    setInterval(updateClock, 1000);
};
startClock()
