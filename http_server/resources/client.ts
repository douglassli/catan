// Incoming message type definitions ***************************************************************

interface Message {
    type: string;
}

interface DeckUpdate {
    wood?: number;
    brick?: number;
    sheep?: number;
    wheat?: number;
    stone?: number;
    devCards?: number;
}

interface StatusUpdate {
    name: string;
    vps?: number;
    roads?: number;
    handSize?: number;
    settles?: number;
    devCards?: number;
    cities?: number;
    roadLength?: number;
    armySize?: number;
    wood?: number;
    brick?: number;
    sheep?: number;
    wheat?: number;
    stone?: number;
}

interface ResourceBlock {
    wood?: number;
    brick?: number;
    sheep?: number;
    wheat?: number;
    stone?: number;
}

interface IncomingMessage extends Message {
    statusUpdates?: StatusUpdate[];
    deckUpdate?: DeckUpdate;
    activeButtons?: string[];
}

interface AvailMessage extends IncomingMessage {
    avail: Coord[];
}

interface AvailSettles extends AvailMessage { type: "AVAIL_SETTLES"; }
interface AvailRoads extends AvailMessage { type: "AVAIL_ROADS"; }
interface AvailCities extends AvailMessage { type: "AVAIL_CITIES"; }
interface AvailRobbers extends AvailMessage { type: "AVAIL_ROBBERS"; }

interface BuiltMessage extends IncomingMessage {
    row: number;
    col: number;
    color: string;
}

interface SettleBuilt extends BuiltMessage { type: "SETTLE_BUILT"; }
interface RoadBuilt extends BuiltMessage { type: "ROAD_BUILT"; }
interface CityBuilt extends BuiltMessage { type: "CITY_BUILT"; }

interface ModelPlayer {
    name: string;
    color: string;
    isReady: boolean;
}

interface CreatedRoom extends IncomingMessage {
    type: "CREATED_ROOM";
    roomID: number;
    playerID: string;
    color: string;
}

interface JoinedRoom extends IncomingMessage {
    type: "JOINED_ROOM";
    playerID: string;
    color: string;
    otherPlayers: ModelPlayer[];
}

interface PlayerJoined extends IncomingMessage {
    type: "PLAYER_JOINED";
    name: string;
    color: string;
}

interface ReadySuccess extends IncomingMessage {
    type: "READY_SUCCESS";
}

interface PlayerReady extends IncomingMessage {
    type: "PLAYER_READY";
    name: string;
}

interface GameStart extends IncomingMessage {
    type: "GAME_START";
    portsHTML: string;
    tilesHTML: string;
    numbersHTML: string;
    playersHTML: string;
    startingPlayer: string;
}

interface TurnStart extends IncomingMessage {
    type: "TURN_START";
    name: string;
}

interface DiceRolled extends IncomingMessage {
    type: "DICE_ROLLED";
    rollNum1: number;
    rollNum2: number;
}

interface RobberMoved extends IncomingMessage {
    type: "ROBBER_MOVED";
    row: number;
    col: number;
    prevRow: number;
    prevCol: number;
    availToRob?: string[];
}

interface PlayerRobbed extends IncomingMessage {
    type: "PLAYER_ROBBED";
    playerRobbed: string;
    playerGained: string;
}

interface BoughtDevCard extends IncomingMessage {
    type: "BOUGHT_DEV_CARD";
    name: string;
}

interface TradeProposed extends IncomingMessage {
    type: "TRADE_PROPOSED";
    tradeId: number;
    name: string;
    curResources: ResourceBlock;
    otherResources: ResourceBlock;
}

interface TradeResponded extends IncomingMessage {
    type: "TRADE_RESPONDED";
    tradeId: number;
    name: string;
    accepted: boolean;
}

interface TradeClosed extends IncomingMessage {
    type: "TRADE_CLOSED";
    tradeId: number;
}

// Outgoing Messsage type definitions **************************************************************

interface IDMessage extends Message {
    playerID: string;
    roomID: number;
}

const enum SelectTypes {
    ROAD = "START_ROAD_SELECT",
    SETTLE = "START_SETTLE_SELECT",
    CITY = "START_CITY_SELECT"
}

interface Ready extends IDMessage { type: "READY"; }
interface StartGame extends IDMessage { type: "START_GAME"; }
interface SettleSelectStart extends IDMessage { type: SelectTypes.SETTLE; }
interface CitySelectStart extends IDMessage { type: SelectTypes.CITY; }
interface RoadSelectStart extends IDMessage { type: SelectTypes.ROAD; }
interface EndTurn extends IDMessage { type: "END_TURN"; }
interface RollDice extends IDMessage { type: "ROLL_DICE"; }
interface BuyDevCard extends IDMessage { type: "BUY_DEV_CARD"; }
interface ChosePlayerRob extends IDMessage { type: "CHOSE_PLAYER_ROB"; name: string; };

interface ChoseMessage extends IDMessage {
    row: number;
    col: number;
}

interface ProposeTrade extends IDMessage {
    type: "PROPOSE_TRADE";
    tradeId: number;
    curResources: ResourceBlock;
    otherResources: ResourceBlock;
}

// This is for other players to decide whether they are willing to accept this trade
interface TradeResponse extends IDMessage {
    type: "TRADE_RESPONSE";
    tradeId: number;
    accepted: boolean;
}

// This is for the current player to choose which of the other players that accepted to trade with
interface ConfirmTrade extends IDMessage {
    type: "CONFIRM_TRADE";
    tradeId: number;
    name: string;
}

interface CancelTrade extends IDMessage {
    type: "CANCEL_TRADE";
    tradeId: number;
}

const enum ChoseTypes {
    ROAD = "CHOSE_ROAD",
    SETTLE = "CHOSE_SETTLE",
    CITY = "CHOSE_CITY",
    ROBBER = "CHOSE_ROBBER"
}

interface ChoseSettle extends ChoseMessage { type: ChoseTypes.SETTLE; }
interface ChoseCity extends ChoseMessage { type: ChoseTypes.CITY; }
interface ChoseRoad extends ChoseMessage { type: ChoseTypes.ROAD; }
interface ChoseRobber extends ChoseMessage { type: ChoseTypes.ROBBER; }

interface CreateRoom extends Message {
    type: "CREATE_ROOM";
    name: string;
}

interface JoinRoom extends Message {
    type: "JOIN_ROOM";
    name: string;
    roomID: number;
}

type OutputMessage = CreateRoom | JoinRoom | IDMessage;

const enum Items {
    PATH = "path",
    SETTLE = "settle",
    CITY = "city",
    ROBBER = "robber"
}

const enum ItemState {
    ACTIVE = "active",
    SELECTING = "selecting",
    HIDDEN = "hidden"
}

type Coord = [number, number];

// Web socket initialization ***********************************************************************

const socket: WebSocket = new WebSocket('ws://localhost:8765');

socket.addEventListener('open', (event: Event) => {console.log("Connection open");});

socket.addEventListener('message', (event: MessageEvent) => {
    const msgHandler: MessageHandler = new MessageHandler();
    const msg: IncomingMessage = JSON.parse(event.data);
    if (typeof msg.statusUpdates !== "undefined") {
        msgHandler.updateStatuses(msg.statusUpdates);
    }
    if (typeof msg.deckUpdate !== "undefined") {
        msgHandler.updateDeckStatus(msg.deckUpdate);
    }
    if (typeof msg.activeButtons !== "undefined") {
        msgHandler.updateActiveButtons(msg.activeButtons);
    }
    msgHandler[msg.type](msg);
});

function sendMessage(msg: OutputMessage): void {
    socket.send(JSON.stringify(msg));
}

// Message Handler Code ****************************************************************************

class MessageHandler {
    updateStatuses(statuses: StatusUpdate[]): void {
        for (let status of statuses) {
            updateStatVal(`${status.name}VPSpan`, 'vps', status);
            updateStatVal(`${status.name}RoadSpan`, 'roads', status);
            updateStatVal(`${status.name}HandSpan`, 'handSize', status);
            updateStatVal(`${status.name}SettleSpan`, 'settles', status);
            updateStatVal(`${status.name}DevSpan`, 'devCards', status);
            updateStatVal(`${status.name}CitySpan`, 'cities', status);
            updateStatVal(`${status.name}RoadLengthSpan`, 'roadLength', status);
            updateStatVal(`${status.name}ArmySpan`, 'armySize', status);
            updateStatVal(`${status.name}WoodSpan`, 'wood', status);
            updateStatVal(`${status.name}BrickSpan`, 'brick', status);
            updateStatVal(`${status.name}SheepSpan`, 'sheep', status);
            updateStatVal(`${status.name}WheatSpan`, 'wheat', status);
            updateStatVal(`${status.name}StoneSpan`, 'stone', status);
        }
    }

    updateDeckStatus(status: DeckUpdate): void {
        updateStatVal("deckDevNumSpan", 'devCards', status);
        updateStatVal("deckWoodNumSpan", 'wood', status);
        updateStatVal("deckBrickNumSpan", 'brick', status);
        updateStatVal("deckSheepNumSpan", 'sheep', status);
        updateStatVal("deckWheatNumSpan", 'wheat', status);
        updateStatVal("deckStoneNumSpan", 'stone', status);
    }

    updateActiveButtons(buttonIds: string[]): void {
        setButtonsDisabled(true);
        for (let bid of buttonIds) {
            const button: HTMLButtonElement = document.getElementById(bid) as HTMLButtonElement;
            button.disabled = false;
        }
    }

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
        for (let i = 0; i < others.length; i++) {
            const player = others[i];
            if (player.name === msg.name) {
                player.isReady = true;
                displayReady(i + 1);
            }
        }
    }

    GAME_START(msg: GameStart): void {
        document.body.classList.add("oceanBg");
        document.getElementById("container").remove();
        document.getElementById("portTiles").innerHTML = msg.portsHTML;
        document.getElementById("tiles").innerHTML = msg.tilesHTML;
        document.getElementById("numbers").innerHTML = msg.numbersHTML;
        document.getElementById("playerBar").innerHTML = msg.playersHTML;
        document.getElementById("svgBoard").classList.remove("hidden");
        document.getElementById("buttonBar").classList.remove("hidden");
        document.getElementById("deckStatus").classList.remove("hidden");
        document.getElementById("lastRollDiv").classList.remove("hidden");
        this.TURN_START({type: "TURN_START", name: msg.startingPlayer});
    }

    AVAIL_SETTLES(msg: AvailSettles): void {
        setButtonsDisabled(true);
        displaySelection(msg.avail, Items.SETTLE, ChoseTypes.SETTLE);
    }

    AVAIL_CITIES(msg: AvailCities): void {
        setButtonsDisabled(true);
        displaySelection(msg.avail, Items.CITY, ChoseTypes.CITY);
    }

    AVAIL_ROADS(msg: AvailRoads): void {
        setButtonsDisabled(true);
        displaySelection(msg.avail, Items.PATH, ChoseTypes.ROAD);
    }

    SETTLE_BUILT(msg: SettleBuilt): void {
        setState([msg.row, msg.col], Items.SETTLE, ItemState.ACTIVE, null);
        getItem([msg.row, msg.col], Items.SETTLE).style.fill = msg.color;
    }

    CITY_BUILT(msg: CityBuilt): void {
        setState([msg.row, msg.col], Items.SETTLE, ItemState.HIDDEN, null);
        setState([msg.row, msg.col], Items.CITY, ItemState.ACTIVE, null);
        getItem([msg.row, msg.col], Items.CITY).style.fill = msg.color;
    }

    ROAD_BUILT(msg: RoadBuilt): void {
        setState([msg.row, msg.col], Items.PATH, ItemState.ACTIVE, null);
        getItem([msg.row, msg.col], Items.PATH).style.fill = msg.color;
    }

    TURN_START(msg: TurnStart): void {
        document.getElementById(`${username}Table`).classList.remove("active");
        for (let plyr of others) {
            document.getElementById(`${plyr.name}Table`).classList.remove("active");
        }
        document.getElementById(`${msg.name}Table`).classList.add("active");
        // TODO: Remove all active trades
    }

    DICE_ROLLED(msg: DiceRolled): void {
        document.getElementById("dice1").innerHTML = msg.rollNum1.toString(10);
        document.getElementById("dice2").innerHTML = msg.rollNum2.toString(10);
    }

    AVAIL_ROBBERS(msg: AvailRobbers): void {
        setButtonsDisabled(true);
        displaySelection(msg.avail, Items.ROBBER, ChoseTypes.ROBBER);
    }

    ROBBER_MOVED(msg: RobberMoved): void {
        setState([msg.row, msg.col], Items.ROBBER, ItemState.ACTIVE, null);
        setState([msg.prevRow, msg.prevCol], Items.ROBBER, ItemState.HIDDEN, null);
        if (typeof msg.availToRob !== "undefined") {
            startPlayerRobSelection(msg.availToRob);
        }
    }

    BOUGHT_DEV_CARD(msg: BoughtDevCard): void {
        // Do nothing
    }

    PLAYER_ROBBED(msg: PlayerRobbed): void {
        // Do nothing
    }
}

// Waiting Room Code *******************************************************************************
let playerId: string;
let roomId: number;
let username: string;
let usercolor: string;
let others: ModelPlayer[] = [];

function addRoomId(): void {
    document.getElementById("roomHeader").innerHTML = `Room ID: ${roomId}`;
}

function addOtherPlayers(): void {
    for (let i = 0; i < others.length; i++) {
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
    sendMessage({type: "CREATE_ROOM", name: username});
}

function joinRoom(): void {
    username = (document.getElementById('nameInput') as HTMLInputElement).value;
    roomId = parseInt((document.getElementById('roomIdInput') as HTMLInputElement).value, 10);
    sendMessage({type: "JOIN_ROOM", name: username, roomID: roomId});
}

function markReady(): void {
    displayReady(0);
    sendMessage({type: "READY", playerID: playerId, roomID: roomId});
}

function startGame(): void {
    if (others.length < 3) {
        return;
    }
    for (let i = 0; i < others.length; i++) {
        if (!others[i].isReady) {
            return;
        }
    }
    sendMessage({type: "START_GAME", playerID: playerId, roomID: roomId});
}

// SVG View code ***********************************************************************************

function setState(coord: Coord, itemType: Items, state: ItemState, clickHandler: (coord: Coord, itemType: Items) => void): void {
    const item: HTMLElement = getItem(coord, itemType);
    const cl: DOMTokenList = item.classList;
    item.onclick = () => {clickHandler(coord, itemType);};
    cl.remove(`active_${itemType}`, ItemState.HIDDEN, ItemState.SELECTING);
    cl.add(state === ItemState.ACTIVE ? `active_${itemType}` : state);
}

function getItem(coord: Coord, itemType: Items): HTMLElement {
    return document.getElementById(`${itemType}${coord[0]}_${coord[1]}`);
}

function setButtonsDisabled(isDisabled: boolean): void {
    const buttons: HTMLCollectionOf<HTMLButtonElement> = document.getElementById("buttonBar").children as HTMLCollectionOf<HTMLButtonElement>;
    for (let i = 0; i < buttons.length; i++) {
        buttons.item(i).disabled = isDisabled;
    }
}

function startSelection(msg_type: SelectTypes): void { sendMessage({type: msg_type, playerID: playerId, roomID: roomId}); }
function startSettleSelection(): void { startSelection(SelectTypes.SETTLE); }
function startCitySelection(): void { startSelection(SelectTypes.CITY); }
function startRoadSelection(): void { startSelection(SelectTypes.ROAD); }

function displaySelection(available: Coord[], itemType: Items, msgType: ChoseTypes): void {
    const handler = (coord, iT) => {handleSelect(coord, iT, available, msgType);};
    for (let availCoord of available) {
        setState(availCoord, itemType, ItemState.SELECTING, handler);
    }
}

function handleSelect(coord: Coord, itemType: Items, available: Coord[], msgType: ChoseTypes) {
    for (let availCoord of available) {
        setState(availCoord, itemType, ItemState.HIDDEN, null);
    }
    setState(coord, itemType, ItemState.ACTIVE, null);
    sendMessage({type: msgType, roomID: roomId, playerID: playerId, row: coord[0], col: coord[1]} as OutputMessage);
}

function endTurn() {
    setButtonsDisabled(true);
    sendMessage({type: "END_TURN", roomID: roomId, playerID: playerId});
}

function rollDice() { sendMessage({type: "ROLL_DICE", roomID: roomId, playerID: playerId}); }

function updateStatVal(id: string, fieldName: string, status: any): void {
    if (typeof status[fieldName] !== "undefined") {
        document.getElementById(id).innerHTML = status[fieldName].toString();
    }
}

function buyDevCard() {
    sendMessage({type: "BUY_DEV_CARD", roomID: roomId, playerID: playerId})
}

function startPlayerRobSelection(avail: string[]): void {
    const robDiv: HTMLElement = document.getElementById("robButtonsDiv");
    robDiv.innerHTML = "";
    for (let name of avail) {
        const button: HTMLButtonElement = document.createElement("button") as HTMLButtonElement;
        button.innerHTML = name;
        button.onclick = () => { handlePlayerRobSelect(name); };
        robDiv.appendChild(button);
    }
    document.getElementById("robWindow").classList.remove("hidden");
}

function handlePlayerRobSelect(name: string): void {
    document.getElementById("robWindow").classList.add("hidden");
    const msg: ChosePlayerRob = {type: "CHOSE_PLAYER_ROB", roomID: roomId, playerID: playerId, name: name};
    sendMessage(msg);
}
