function makeUrl(host, path) {
    return `http://${host}/${path}`;
}

async function getRequest(url) {
    const response = await fetch(url);
    return response.json();
}

async function postRequest(url: string, data: object) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return response.json();
}

interface ModelPlayer {
    name: string;
    color: string;
    isReady: boolean;
}

const HOST: string = "127.0.0.1:8080";
var playerId: string;
var roomId: number;
var username: string;
var usercolor: string;
var others: ModelPlayer[] = [];

function addRoomId(): void {
    document.getElementById("roomHeader").innerHTML = `Room ID: ${roomId}`;
}

function addOtherPlayers(): void {
    for (var i = 0; i < others.length; i++) {
        const plyr = others[i];
        appendPlayer(plyr.name, plyr.color, plyr.isReady);
    }
}

function appendPlayer(playerName: string, playerColor: string, playerReady: boolean): void {
    var playerList: HTMLElement = document.getElementById('playerList');
    var newPlayer: HTMLElement = document.createElement("li");

    var nameText: Text = document.createTextNode("Name: ");
    var colorText: Text = document.createTextNode(", Color: ");
    var readyText: Text = document.createTextNode(", Ready: ");

    var nameSpan: HTMLElement = document.createElement("span");
    nameSpan.id = `${playerName}_NameSpan`;
    nameSpan.innerHTML = playerName;

    var colorSpan: HTMLElement = document.createElement("span");
    colorSpan.id = `${playerName}_ColorSpan`;
    colorSpan.innerHTML = playerColor;

    var readySpan: HTMLElement = document.createElement("span");
    readySpan.id = `${playerName}_ReadySpan`;
    readySpan.innerHTML = playerName;

    newPlayer.appendChild(nameText);
    newPlayer.appendChild(nameSpan);
    newPlayer.appendChild(colorText);
    newPlayer.appendChild(colorSpan);
    newPlayer.appendChild(readyText);
    newPlayer.appendChild(readySpan);

    playerList.appendChild(newPlayer);
}

function displayReady(playerName: string): void {
    var readySpan: HTMLElement = document.getElementById(`${playerName}_ReadySpan`);
    readySpan.innerHTML = true.toString();
}

function createRoom(): void {
    username = (document.getElementById('nameInput') as HTMLInputElement).value;
    var out: CreateRoom = {name: username};
    const resp = postRequest(makeUrl(HOST, "rooms/create-room"), out);
    roomId = resp.roomID;
    playerId = resp.playerID;
    usercolor = resp.color;
    addRoomId();
    appendPlayer(username, usercolor, false);
}

function joinRoom(): void {
    username = (document.getElementById('nameInput') as HTMLInputElement).value;
    roomId = parseInt((document.getElementById('roomIdInput') as HTMLInputElement).value, 10);
    var out: JoinRoom = {name: username, roomID: roomId};
    const resp = postRequest(makeUrl(HOST, "rooms/join-room"), out);
    playerId = resp.playerID;
    usercolor = resp.color;
    others = resp.otherPlayers;
    addRoomId();
    appendPlayer(username, usercolor, false);
    addOtherPlayers();
}

function markReady(): void {
    displayReady(username);
    var out: Ready = {playerID: playerId, roomID: roomId};
    const resp = postRequest(makeUrl(HOST, "rooms/mark-ready"), out);
}
