// signature.js

async function Signature(signature, model="User") {
    try {
        const response = await fetch('/getacc', {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({"signature":signature, "model":model})
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log(data);

        return data.response;
    } catch (error) {
        console.log('There was a problem with the fetch operation:', error);
        return null;
    }
};
