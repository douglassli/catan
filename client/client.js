// Outgoing types
const CREATE_ROOM = "CREATE_ROOM"
const JOIN_ROOM = "JOIN_ROOM"
const READY = "READY"

// Incoming types
const CREATED_ROOM = "CREATED_ROOM"
const JOINED_ROOM = "JOINED_ROOM"
const PLAYER_JOINED = "PLAYER_JOINED"
const READY_SUCCESS = "READY_SUCCESS"
const PLAYER_READY = "PLAYER_READY"
const ERROR = "ERROR"


// Create WebSocket connection.
const socket = new WebSocket('ws://localhost:8765');
var playerId;
var roomId;
var username;
var usercolor;
var others = []

// Connection opened
socket.addEventListener('open', function (event) {
    console.log("Connection open")
});

// Listen for messages
socket.addEventListener('message', function (event) {
    var obj = JSON.parse(event.data);

    switch(obj.type) {
        case CREATED_ROOM:
        roomId = obj.roomID;
        playerId = obj.playerID;
        usercolor = obj.color;
        addRoomId();
        appendPlayer(username, usercolor, false);
        break;
        case JOINED_ROOM:
        playerId = obj.playerID;
        usercolor = obj.color;
        others = obj.otherPlayers;
        addRoomId();
        appendPlayer(username, usercolor, false);
        addOtherPlayers();
        break;
        case PLAYER_JOINED:
        others.push({name: obj.name, color: obj.color, isReady: false});
        appendPlayer(obj.name, obj.color, false);
        break;
        case READY_SUCCESS:
        // do nothing
        break;
        case PLAYER_READY:
        displayReady(obj.name);
        break;
        default:
        // code block
    };

    console.log(obj);
});

function addRoomId() {
    document.getElementById("roomHeader").innerHTML = `Room ID: ${roomId}`;
}

function addOtherPlayers() {
    var playerList = document.getElementById('playerList');
    console.log(others)
    for (var i = 0; i < others.length; i++) {
        const plyr = others[i];
        console.log(plyr)
        appendPlayer(plyr.name, plyr.color, plyr.isReady);
    }
}

function appendPlayer(playerName, playerColor, playerReady) {
    var playerList = document.getElementById('playerList');
    var newPlayer = document.createElement("li");

    var nameText = document.createTextNode("Name: ");
    var colorText = document.createTextNode(", Color: ");
    var readyText = document.createTextNode(", Ready: ");

    var nameSpan = document.createElement("span");
    nameSpan.id = `${playerName}_NameSpan`;
    nameSpan.innerHTML = `${playerName}`;

    var colorSpan = document.createElement("span");
    colorSpan.id = `${playerName}_ColorSpan`;
    colorSpan.innerHTML = `${playerColor}`;

    var readySpan = document.createElement("span");
    readySpan.id = `${playerName}_ReadySpan`;
    readySpan.innerHTML = `${playerReady}`;

    newPlayer.appendChild(nameText);
    newPlayer.appendChild(nameSpan);
    newPlayer.appendChild(colorText);
    newPlayer.appendChild(colorSpan);
    newPlayer.appendChild(readyText);
    newPlayer.appendChild(readySpan);

    playerList.appendChild(newPlayer);
}

function displayReady(playerName) {
    var readySpan = document.getElementById(`${playerName}_ReadySpan`);
    readySpan.innerHTML = `${true}`;
}

function createRoom() {
    username = document.getElementById('nameInput').value;
    var out = {type: CREATE_ROOM, name: username};
    socket.send(JSON.stringify(out));
}

function joinRoom() {
    username = document.getElementById('nameInput').value;
    roomId = parseInt(document.getElementById('roomIdInput').value, 10);
    var out = {type: JOIN_ROOM, name: username, roomID: roomId};
    socket.send(JSON.stringify(out));
}

function markReady() {
    displayReady(username);
    var out = {type: READY, playerID: playerId, roomID: roomId};
    socket.send(JSON.stringify(out));
}
