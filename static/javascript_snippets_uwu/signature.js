// signature.js

// for the new signature system
function Signature(signature) {
    fetch('/getacc', {
        method: 'POST',
        headers: {'Content-Type': 'application/json',},
        body: JSON.stringify(signature),})
    .then(response => response.json())
    .then(data => {
        console.log('POST response:', data);
        account = data.response
    })
    return account;
};
