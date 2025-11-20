// signature.js

// for the new signature system
async function fetchSignature(signature) {
    try {
        const response = await fetch('/getacc', {method: "POST", headers: {'Content-Type': 'application/json'}, body:JSON.stringify(signature)});
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        let data = await response.json();
        console.log(data);
        return data; // The data is returned here
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
};
function Signature(signature) {
    fetchSignature(signature).then(result => {
        if (result) {
            return Array.from(result.response);
        };
    });
};
