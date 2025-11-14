function updateClock() {
    const now = new Date();
    const formattedTime = now.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
        hour12: false
        });
    const formattedDate = now.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
        });

    document.getElementById('clock-display').innerText = `${formattedDate} ${formattedTime}`;
};
function startClock() {
    setInterval(updateClock, 1000);
};


//maybe useful functions
function setText(elem, text) {
    document.getElementById("elem").innerText = text;
};

function byId(elem) {
    return document.getElementById(elem);
};
