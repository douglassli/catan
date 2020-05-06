
const testData: ModelData = JSON.parse('{"tiles": [{"row": 0, "col": 0, "resource": "DESERT", "rollNum": null, "hasRobber": true}, {"row": 0, "col": 1, "resource": "WOOD", "rollNum": 3, "hasRobber": false}, {"row": 0, "col": 2, "resource": "BRICK", "rollNum": 6, "hasRobber": false}, {"row": 1, "col": 0, "resource": "STONE", "rollNum": 6, "hasRobber": false}, {"row": 1, "col": 1, "resource": "STONE", "rollNum": 8, "hasRobber": false}, {"row": 1, "col": 2, "resource": "SHEEP", "rollNum": 11, "hasRobber": false}, {"row": 1, "col": 3, "resource": "WHEAT", "rollNum": 9, "hasRobber": false}, {"row": 2, "col": 0, "resource": "WHEAT", "rollNum": 4, "hasRobber": false}, {"row": 2, "col": 1, "resource": "WHEAT", "rollNum": 12, "hasRobber": false}, {"row": 2, "col": 2, "resource": "SHEEP", "rollNum": 5, "hasRobber": false}, {"row": 2, "col": 3, "resource": "STONE", "rollNum": 10, "hasRobber": false}, {"row": 2, "col": 4, "resource": "BRICK", "rollNum": 9, "hasRobber": false}, {"row": 3, "col": 0, "resource": "WOOD", "rollNum": 10, "hasRobber": false}, {"row": 3, "col": 1, "resource": "SHEEP", "rollNum": 3, "hasRobber": false}, {"row": 3, "col": 2, "resource": "WOOD", "rollNum": 4, "hasRobber": false}, {"row": 3, "col": 3, "resource": "WOOD", "rollNum": 2, "hasRobber": false}, {"row": 4, "col": 0, "resource": "WHEAT", "rollNum": 5, "hasRobber": false}, {"row": 4, "col": 1, "resource": "BRICK", "rollNum": 8, "hasRobber": false}, {"row": 4, "col": 2, "resource": "SHEEP", "rollNum": 11, "hasRobber": false}], "paths": [{"row": 7, "col": 3, "hasRoad": false, "owner": ""}, {"row": 4, "col": 7, "hasRoad": false, "owner": ""}, {"row": 6, "col": 9, "hasRoad": false, "owner": ""}, {"row": 1, "col": 3, "hasRoad": false, "owner": ""}, {"row": 9, "col": 1, "hasRoad": false, "owner": ""}, {"row": 4, "col": 8, "hasRoad": false, "owner": ""}, {"row": 3, "col": 0, "hasRoad": false, "owner": ""}, {"row": 6, "col": 6, "hasRoad": false, "owner": ""}, {"row": 8, "col": 0, "hasRoad": false, "owner": ""}, {"row": 2, "col": 1, "hasRoad": false, "owner": ""}, {"row": 6, "col": 2, "hasRoad": false, "owner": ""}, {"row": 5, "col": 1, "hasRoad": false, "owner": ""}, {"row": 2, "col": 5, "hasRoad": false, "owner": ""}, {"row": 0, "col": 3, "hasRoad": false, "owner": ""}, {"row": 10, "col": 3, "hasRoad": false, "owner": ""}, {"row": 2, "col": 4, "hasRoad": false, "owner": ""}, {"row": 7, "col": 2, "hasRoad": false, "owner": ""}, {"row": 4, "col": 0, "hasRoad": false, "owner": ""}, {"row": 1, "col": 2, "hasRoad": false, "owner": ""}, {"row": 8, "col": 5, "hasRoad": false, "owner": ""}, {"row": 9, "col": 0, "hasRoad": false, "owner": ""}, {"row": 6, "col": 7, "hasRoad": false, "owner": ""}, {"row": 3, "col": 3, "hasRoad": false, "owner": ""}, {"row": 4, "col": 9, "hasRoad": false, "owner": ""}, {"row": 5, "col": 5, "hasRoad": false, "owner": ""}, {"row": 8, "col": 1, "hasRoad": false, "owner": ""}, {"row": 4, "col": 4, "hasRoad": false, "owner": ""}, {"row": 10, "col": 2, "hasRoad": false, "owner": ""}, {"row": 6, "col": 3, "hasRoad": false, "owner": ""}, {"row": 5, "col": 0, "hasRoad": false, "owner": ""}, {"row": 2, "col": 2, "hasRoad": false, "owner": ""}, {"row": 3, "col": 4, "hasRoad": false, "owner": ""}, {"row": 8, "col": 6, "hasRoad": false, "owner": ""}, {"row": 10, "col": 0, "hasRoad": false, "owner": ""}, {"row": 0, "col": 4, "hasRoad": false, "owner": ""}, {"row": 4, "col": 1, "hasRoad": false, "owner": ""}, {"row": 1, "col": 1, "hasRoad": false, "owner": ""}, {"row": 6, "col": 4, "hasRoad": false, "owner": ""}, {"row": 5, "col": 4, "hasRoad": false, "owner": ""}, {"row": 2, "col": 6, "hasRoad": false, "owner": ""}, {"row": 3, "col": 2, "hasRoad": false, "owner": ""}, {"row": 10, "col": 4, "hasRoad": false, "owner": ""}, {"row": 0, "col": 0, "hasRoad": false, "owner": ""}, {"row": 7, "col": 1, "hasRoad": false, "owner": ""}, {"row": 4, "col": 5, "hasRoad": false, "owner": ""}, {"row": 8, "col": 2, "hasRoad": false, "owner": ""}, {"row": 9, "col": 3, "hasRoad": false, "owner": ""}, {"row": 6, "col": 0, "hasRoad": false, "owner": ""}, {"row": 2, "col": 3, "hasRoad": false, "owner": ""}, {"row": 0, "col": 5, "hasRoad": false, "owner": ""}, {"row": 8, "col": 7, "hasRoad": false, "owner": ""}, {"row": 10, "col": 1, "hasRoad": false, "owner": ""}, {"row": 4, "col": 2, "hasRoad": false, "owner": ""}, {"row": 1, "col": 0, "hasRoad": false, "owner": ""}, {"row": 6, "col": 5, "hasRoad": false, "owner": ""}, {"row": 5, "col": 3, "hasRoad": false, "owner": ""}, {"row": 0, "col": 1, "hasRoad": false, "owner": ""}, {"row": 2, "col": 7, "hasRoad": false, "owner": ""}, {"row": 10, "col": 5, "hasRoad": false, "owner": ""}, {"row": 8, "col": 3, "hasRoad": false, "owner": ""}, {"row": 7, "col": 0, "hasRoad": false, "owner": ""}, {"row": 4, "col": 6, "hasRoad": false, "owner": ""}, {"row": 6, "col": 8, "hasRoad": false, "owner": ""}, {"row": 9, "col": 2, "hasRoad": false, "owner": ""}, {"row": 6, "col": 1, "hasRoad": false, "owner": ""}, {"row": 3, "col": 1, "hasRoad": false, "owner": ""}, {"row": 7, "col": 4, "hasRoad": false, "owner": ""}, {"row": 2, "col": 0, "hasRoad": false, "owner": ""}, {"row": 4, "col": 3, "hasRoad": false, "owner": ""}, {"row": 5, "col": 2, "hasRoad": false, "owner": ""}, {"row": 0, "col": 2, "hasRoad": false, "owner": ""}, {"row": 8, "col": 4, "hasRoad": false, "owner": ""}], "nodes": [{"row": 4, "col": 7, "building": "", "owner": ""}, {"row": 1, "col": 3, "building": "", "owner": ""}, {"row": 4, "col": 8, "building": "", "owner": ""}, {"row": 3, "col": 0, "building": "", "owner": ""}, {"row": 2, "col": 8, "building": "", "owner": ""}, {"row": 5, "col": 6, "building": "", "owner": ""}, {"row": 2, "col": 1, "building": "", "owner": ""}, {"row": 1, "col": 6, "building": "", "owner": ""}, {"row": 3, "col": 7, "building": "", "owner": ""}, {"row": 0, "col": 3, "building": "", "owner": ""}, {"row": 2, "col": 5, "building": "", "owner": ""}, {"row": 5, "col": 1, "building": "", "owner": ""}, {"row": 2, "col": 4, "building": "", "owner": ""}, {"row": 4, "col": 0, "building": "", "owner": ""}, {"row": 1, "col": 2, "building": "", "owner": ""}, {"row": 3, "col": 3, "building": "", "owner": ""}, {"row": 2, "col": 9, "building": "", "owner": ""}, {"row": 5, "col": 5, "building": "", "owner": ""}, {"row": 3, "col": 10, "building": "", "owner": ""}, {"row": 4, "col": 4, "building": "", "owner": ""}, {"row": 1, "col": 5, "building": "", "owner": ""}, {"row": 3, "col": 6, "building": "", "owner": ""}, {"row": 2, "col": 2, "building": "", "owner": ""}, {"row": 0, "col": 4, "building": "", "owner": ""}, {"row": 5, "col": 0, "building": "", "owner": ""}, {"row": 4, "col": 1, "building": "", "owner": ""}, {"row": 1, "col": 1, "building": "", "owner": ""}, {"row": 3, "col": 2, "building": "", "owner": ""}, {"row": 0, "col": 0, "building": "", "owner": ""}, {"row": 2, "col": 6, "building": "", "owner": ""}, {"row": 5, "col": 4, "building": "", "owner": ""}, {"row": 4, "col": 5, "building": "", "owner": ""}, {"row": 5, "col": 2, "building": "", "owner": ""}, {"row": 1, "col": 4, "building": "", "owner": ""}, {"row": 2, "col": 10, "building": "", "owner": ""}, {"row": 3, "col": 9, "building": "", "owner": ""}, {"row": 0, "col": 5, "building": "", "owner": ""}, {"row": 2, "col": 3, "building": "", "owner": ""}, {"row": 4, "col": 2, "building": "", "owner": ""}, {"row": 1, "col": 0, "building": "", "owner": ""}, {"row": 3, "col": 5, "building": "", "owner": ""}, {"row": 0, "col": 1, "building": "", "owner": ""}, {"row": 2, "col": 7, "building": "", "owner": ""}, {"row": 5, "col": 3, "building": "", "owner": ""}, {"row": 4, "col": 6, "building": "", "owner": ""}, {"row": 3, "col": 1, "building": "", "owner": ""}, {"row": 3, "col": 8, "building": "", "owner": ""}, {"row": 0, "col": 6, "building": "", "owner": ""}, {"row": 1, "col": 8, "building": "", "owner": ""}, {"row": 2, "col": 0, "building": "", "owner": ""}, {"row": 4, "col": 3, "building": "", "owner": ""}, {"row": 1, "col": 7, "building": "", "owner": ""}, {"row": 3, "col": 4, "building": "", "owner": ""}, {"row": 0, "col": 2, "building": "", "owner": ""}]}');

interface ModelTile {
    row: number;
    col: number;
    resource: string;
    rollNum: number;
    hasRobber: boolean;
}

interface ModelPath {
    row: number;
    col: number;
    hasRoad: boolean;
    owner: string;
}

interface ModelNode {
    row: number;
    col: number;
    building: string;
    owner: string;
}

interface ModelData {
    tiles: ModelTile[];
    paths: ModelPath[];
    nodes: ModelNode[];
}

interface HexTilePair {
    hexTiles: HexTile[];
    bgTiles: HexTile[];
}

const canWidth: number = 750;
const canHeight: number = 750;
const numRows: number = 5;
const padding: number = 10;
const hexLen: number = 65;
const setRad: number = 13;

const hexWidth: number = hexLen * Math.sqrt(3);
const horizOffset: number = hexWidth + padding;
const vertPad: number = (Math.sqrt(3) * padding) / 2;
const vertOffset: number = (hexLen * 1.5) + vertPad;
const vco: number = padding / Math.sqrt(3);

const colorMap = {
    STONE: "#9c9c9c",
    SHEEP: "#8eb427",
    BRICK: "#de5e30",
    WOOD: "#20953d",
    WHEAT: "#f2ba38",
    DESERT: "#c48d52"
}
const borderColor: string = "#c4a060";
const portColor: string = "#b97c31";

function draw(): void {
    const bgCanvas: HTMLCanvasElement = document.getElementById("bgCanvas") as HTMLCanvasElement;
    const bgCtx: CanvasRenderingContext2D = bgCanvas.getContext("2d");
    initBackground(bgCtx, testData);

    const fgCanvas: HTMLCanvasElement = document.getElementById("fgCanvas") as HTMLCanvasElement;
    const fgCtx = fgCanvas.getContext("2d");
    initForeground(fgCtx, testData);
}

function initBackground(ctx: CanvasRenderingContext2D, data: ModelData): void {
    const tilesObj = initHexTiles(data.tiles);
    const bgTiles = tilesObj.bgTiles;
    const hexTiles = tilesObj.hexTiles;
    for (let i: number = 0; i < bgTiles.length; i++) {
        bgTiles[i].draw(ctx);
    }
    for (let i: number = 0; i < hexTiles.length; i++) {
        hexTiles[i].draw(ctx);
    }
    // TODO: ports
}

function initForeground(ctx: CanvasRenderingContext2D, data: ModelData): void {

}

function initHexTiles(tiles: ModelTile[]): HexTilePair {
    const out: HexTilePair = {
        hexTiles: [],
        bgTiles: []
    };

    const boardWidth: number = (numRows * hexWidth) + ((numRows + 1) * padding);
    const boardHeight: number = ((numRows - 1) * vertOffset) + hexLen * 2;
    const initX: number = ((canWidth - boardWidth) / 2) + horizOffset / 2;
    const initY: number = (canHeight - boardHeight) / 2;

    for (let i: number = 0; i < tiles.length; i++) {
        const curTile: ModelTile = tiles[i];
        const color: string = colorMap[curTile.resource];
        const initXOffset: number = initX + Math.abs(curTile.row - Math.floor(numRows / 2)) * (horizOffset / 2);
        const x: number = initXOffset + horizOffset * curTile.col;
        const y: number = initY + curTile.row * vertOffset;

        const hexTile: HexTile = new HexTile(curTile.row, curTile.col, x, y, hexLen, color, curTile.rollNum);
        const bgTile: HexTile = new HexTile(curTile.row, curTile.col, x, y - 2 * vco, hexLen + 2 * vco, borderColor, null);
        out.hexTiles.push(hexTile);
        out.bgTiles.push(bgTile);
    }

    return out;
}

function radians(degrees: number): number {
    return degrees * Math.PI / 180;
}

class HexTile {
    row: number;
    col: number;
    hexCoords: number[];
    color: string;
    rollNum: number;
    numTileLen: number;
    numTileX: number;
    numTileY: number;
    numColor: string;
    numX: number;
    numY: number;
    numFont: string;

    constructor(row: number, col: number, x: number, y: number, len: number, color: string, rollNum: number) {
        this.row = row;
        this.col = col;
        this.hexCoords = [x, y];
        for (let i: number = 1; i < 6; i++) {
            const nx: number = this.hexCoords[i * 2 - 2] + len * Math.cos(radians(60 * (i - 1) + 30));
            const ny: number = this.hexCoords[i * 2 - 1] + len * Math.sin(radians(60 * (i - 1) + 30));
            this.hexCoords.push(nx);
            this.hexCoords.push(ny);
        }
        this.color = color;
        this.rollNum = rollNum;
        this.numTileLen = 2 * len / 3;
        this.numTileX = x - this.numTileLen / 2;
        this.numTileY = y + len - (this.numTileLen / 2);
        this.numColor = this.rollNum == 6 || this.rollNum == 8 ? "#ff0000" : "#000000";
        this.numX = x;
        this.numY = y + len;
        this.numFont = `${this.numTileLen / 1.25}px serif`;
    }

    draw(ctx: CanvasRenderingContext2D): void {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.moveTo(this.hexCoords[0], this.hexCoords[1]);
        for (let i: number = 1; i < 6; i++) {
            ctx.lineTo(this.hexCoords[i * 2], this.hexCoords[i * 2 + 1]);
        }
        ctx.fill();

        if (this.rollNum) {
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(this.numTileX, this.numTileY, this.numTileLen, this.numTileLen);

            ctx.fillStyle = this.numColor;
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.font = this.numFont;
            ctx.fillText(this.rollNum.toString(10), this.numX, this.numY);
        }
    }
}
