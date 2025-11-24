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
    let clockDisplay = document.createElement("h1");
    clockDisplay.id = "clock-display";
    clockDisplay.style.position = "relative";
    clockDisplay.style.top = "0px";
    clockDisplay.style.left = "0px";
    clockDisplay.style.margin = "2px";
    clockDisplay.style.padding = "2px";
    clockDisplay.style.width = "fit-content";
    clockDisplay.style.height = "fit-content";
    clockDisplay.style.border = "1px solid black";
    clockDisplay.style.backgroundColor = "white";
    clockDisplay.style.fontSize = "10px";
    clockDisplay.style.textAlign = "left";
    clockDisplay.style.textDecoration = "0px";
    document.body.appendChild(clockDisplay);

    updateClock();
    setInterval(updateClock, 1000);
};
startClock()
