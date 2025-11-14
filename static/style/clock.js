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
    setInterval(updateClock, 1000);
};

