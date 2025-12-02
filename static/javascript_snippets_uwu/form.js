async function form(action="", info_json={}) {
    try {
        const response = await fetch(action, {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(info_json)
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
