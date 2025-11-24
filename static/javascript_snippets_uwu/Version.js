const owner = "DiggyGorgonzola";
const repo = "glorbank";



function createVerBox() {
    let versionBox = document.createElement("div");
    versionBox.id = "version-box";
    versionBox.style.position = "relative";
    versionBox.style.margin = "2px";
    versionBox.style.padding = "2px";
    versionBox.style.top = "0px";
    versionBox.style.left = "0px";
    versionBox.style.width = "fit-content";
    versionBox.style.height = "fit-content";
    versionBox.style.border = "1px solid black";
    versionBox.style.backgroundColor = "white";
    versionBox.style.fontSize = "10px";
    versionBox.style.textAlign = "left";
    versionBox.style.textDecoration = "none";
    document.body.appendChild(versionBox);
};

function createText(text) {
    let versionText = document.createElement("h1");
    versionText.textContent = text;
    versionText.style.fontSize = "10px";
    document.getElementById("version-box").appendChild(versionText);
};
async function GetVer() {
    try {
        const response = await fetch(`https://api.github.com/repos/${owner}/${repo}/commits`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        };

        const commits = await response.json();
        const latestCommit = commits[0]

        console.log("Latest update SHA: ", latestCommit.sha);
        createText("Latest update SHA: " + latestCommit.sha);

        console.log("Author: ", latestCommit.commit.author.name);
        createText("Author: " + latestCommit.commit.author.name);

        console.log("Date: ", latestCommit.commit.author.date);
        createText("Date: " + latestCommit.commit.author.date);

        console.log("Change: ", latestCommit.commit.message);
        createText("Change: " + latestCommit.commit.message);
    } catch (error) {
        console.log(error);
    };
};
createVerBox();
GetVer();
