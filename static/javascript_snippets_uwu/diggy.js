//diggy.js


//maybe useful functions


function setText(elem, text) {
    document.getElementById("elem").innerText = text;
};

function byId(elem) {
    return document.getElementById(elem);
};

function isNumeric(value) {
    return Number.isFinite(Number(value)) && !Number.isNaN(Number(value));
};
