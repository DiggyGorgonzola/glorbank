async function GNB(val) {
    try {
        const response = await fetch('/GNB', {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(val)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log(data);

        return data.response;
    } catch (error) {
        console.log("GNB.js error:", "inp:", val, "err:", error);
        return null;
    }
};
let STL;
let WTP;
let WTD;
let WTUSD;
async function setBankInfo() {
    STL = await GNB("suspicious_transaction_limit");
    WTP = await GNB("woolong_to_parts");
    WTD = await GNB("woolong_to_diamond");
    WTUSD = await GNB("woolong_to_usd");

    console.log(STL, WTP, WTD, WTUSD);
}

setBankInfo();