interface ModelPlayer {
    name: string;
    color: string;
    isReady: boolean;
}

interface CreatedRoom {
    type: "CREATED_ROOM";
    roomID: number;
    playerID: string;
    color: string;
}

interface JoinedRoom {
    type: "JOINED_ROOM";
    playerID: string;
    color: string;
    otherPlayers: ModelPlayer[];
}

interface PlayerJoined {
    type: "PLAYER_JOINED";
    name: string;
    color: string;
}

interface ReadySuccess {
    type: "READY_SUCCESS";
}

interface PlayerReady {
    type: "PLAYER_READY";
    name: string;
}

interface Error {
    type: "ERROR";
}

type InputMessage = CreatedRoom | JoinedRoom | PlayerJoined | ReadySuccess | PlayerReady | Error;

interface CreateRoom {
    type: "CREATE_ROOM";
    name: string;
}

interface JoinRoom {
    type: "JOIN_ROOM";
    name: string;
    roomID: number;
}

interface Ready {
    type: "READY";
    playerID: string;
    roomID: number;
}

type OutputMessage = CreateRoom | JoinRoom | Ready;

// Create WebSocket connection.
const socket: WebSocket = new WebSocket('ws://localhost:8765');
var playerId: string;
var roomId: number;
var username: string;
var usercolor: string;
var others: ModelPlayer[] = [];

// Connection opened
socket.addEventListener('open', function (event: Event): void {
    console.log("Connection open");
});

// Listen for messages
socket.addEventListener('message', function (event: MessageEvent) {
    var obj: InputMessage = JSON.parse(event.data);

    switch(obj.type) {
        case "CREATED_ROOM":
            roomId = obj.roomID;
            playerId = obj.playerID;
            usercolor = obj.color;
            addRoomId();
            appendPlayer(username, usercolor, false);
            break;
        case "JOINED_ROOM":
            playerId = obj.playerID;
            usercolor = obj.color;
            others = obj.otherPlayers;
            addRoomId();
            appendPlayer(username, usercolor, false);
            addOtherPlayers();
            break;
        case "PLAYER_JOINED":
            others.push({name: obj.name, color: obj.color, isReady: false});
            appendPlayer(obj.name, obj.color, false);
            break;
        case "READY_SUCCESS":
            // do nothing
            break;
        case "PLAYER_READY":
            displayReady(obj.name);
            break;
            default:
            // code block
    }
});

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
    var out: CreateRoom = {type: "CREATE_ROOM", name: username};
    sendMessage(out);
}

function joinRoom(): void {
    username = (document.getElementById('nameInput') as HTMLInputElement).value;
    roomId = parseInt((document.getElementById('roomIdInput') as HTMLInputElement).value, 10);
    var out: JoinRoom = {type: "JOIN_ROOM", name: username, roomID: roomId};
    sendMessage(out);
}

function markReady(): void {
    displayReady(username);
    var out: Ready = {type: "READY", playerID: playerId, roomID: roomId};
    sendMessage(out);
}

function sendMessage(msg: OutputMessage): void {
    socket.send(JSON.stringify(msg));
}
