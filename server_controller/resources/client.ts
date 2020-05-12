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

interface GameStart {
    type: "GAME_START";
    boardHTML: string;
}

interface Error {
    type: "ERROR";
}

type InputMessage = CreatedRoom | JoinedRoom | PlayerJoined | ReadySuccess | PlayerReady | GameStart | Error;

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

interface StartGame {
    type: "START_GAME";
    playerID: string;
    roomID: number;
}

type OutputMessage = CreateRoom | JoinRoom | Ready | StartGame;

// Create WebSocket connection.
const socket: WebSocket = new WebSocket('ws://localhost:8765');
socket.addEventListener('open', (event: Event) => {console.log("Connection open");});
socket.addEventListener('message', (event: MessageEvent) => {
    var msg: InputMessage = JSON.parse(event.data);
    new MessageHandler()[msg.type](msg);
});

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
        appendPlayer(plyr.name, plyr.color, plyr.isReady, i + 1);
    }
}

function appendPlayer(playerName: string, playerColor: string, playerReady: boolean, pNum: number): void {
    document.getElementById(`p${pNum}Name`).innerHTML = playerName;
    document.getElementById(`p${pNum}Color`).innerHTML = playerColor;
    document.getElementById(`p${pNum}Ready`).innerHTML = playerReady.toString();
    document.getElementById(`p${pNum}Entry`).hidden = false;
}

function displayReady(pNum: number): void {
    document.getElementById(`p${pNum}Ready`).innerHTML = true.toString();
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
    displayReady(0);
    var out: Ready = {type: "READY", playerID: playerId, roomID: roomId};
    sendMessage(out);
}

function startGame(): void {
    if (others.length < 3) {
        return;
    }
    for (var i = 0; i < others.length; i++) {
        if (!others[i].isReady) {
            return;
        }
    }
    var out: StartGame = {type: "START_GAME", playerID: playerId, roomID: roomId}
    sendMessage(out);
}

function sendMessage(msg: OutputMessage): void {
    socket.send(JSON.stringify(msg));
}

class MessageHandler {
    CREATED_ROOM(msg: CreatedRoom): void {
        roomId = msg.roomID;
        playerId = msg.playerID;
        usercolor = msg.color;
        addRoomId();
        appendPlayer(username, usercolor, false, 0);
    }

    JOINED_ROOM(msg: JoinedRoom): void {
        playerId = msg.playerID;
        usercolor = msg.color;
        others = msg.otherPlayers;
        addRoomId();
        appendPlayer(username, usercolor, false, 0);
        addOtherPlayers();
    }

    PLAYER_JOINED(msg: PlayerJoined): void {
        others.push({name: msg.name, color: msg.color, isReady: false});
        appendPlayer(msg.name, msg.color, false, others.length);
    }

    READY_SUCCESS(msg: ReadySuccess): void {
        // Do nothing
    }

    PLAYER_READY(msg: PlayerReady): void {
        for (var i = 0; i < others.length; i++) {
            var player = others[i];
            if (player.name === msg.name) {
                player.isReady = true;
                displayReady(i + 1);
            }
        }
    }

    GAME_START(msg: GameStart): void {
        document.getElementById("container").innerHTML = msg.boardHTML;
    }
}
