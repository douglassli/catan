
const testData = JSON.parse('{"tiles": [{"row": 0, "col": 0, "resource": "DESERT", "rollNum": null, "hasRobber": true}, {"row": 0, "col": 1, "resource": "WOOD", "rollNum": 3, "hasRobber": false}, {"row": 0, "col": 2, "resource": "BRICK", "rollNum": 6, "hasRobber": false}, {"row": 1, "col": 0, "resource": "STONE", "rollNum": 6, "hasRobber": false}, {"row": 1, "col": 1, "resource": "STONE", "rollNum": 8, "hasRobber": false}, {"row": 1, "col": 2, "resource": "SHEEP", "rollNum": 11, "hasRobber": false}, {"row": 1, "col": 3, "resource": "WHEAT", "rollNum": 9, "hasRobber": false}, {"row": 2, "col": 0, "resource": "WHEAT", "rollNum": 4, "hasRobber": false}, {"row": 2, "col": 1, "resource": "WHEAT", "rollNum": 12, "hasRobber": false}, {"row": 2, "col": 2, "resource": "SHEEP", "rollNum": 5, "hasRobber": false}, {"row": 2, "col": 3, "resource": "STONE", "rollNum": 10, "hasRobber": false}, {"row": 2, "col": 4, "resource": "BRICK", "rollNum": 9, "hasRobber": false}, {"row": 3, "col": 0, "resource": "WOOD", "rollNum": 10, "hasRobber": false}, {"row": 3, "col": 1, "resource": "SHEEP", "rollNum": 3, "hasRobber": false}, {"row": 3, "col": 2, "resource": "WOOD", "rollNum": 4, "hasRobber": false}, {"row": 3, "col": 3, "resource": "WOOD", "rollNum": 2, "hasRobber": false}, {"row": 4, "col": 0, "resource": "WHEAT", "rollNum": 5, "hasRobber": false}, {"row": 4, "col": 1, "resource": "BRICK", "rollNum": 8, "hasRobber": false}, {"row": 4, "col": 2, "resource": "SHEEP", "rollNum": 11, "hasRobber": false}], "paths": [{"row": 7, "col": 3, "hasRoad": false, "owner": ""}, {"row": 4, "col": 7, "hasRoad": false, "owner": ""}, {"row": 6, "col": 9, "hasRoad": false, "owner": ""}, {"row": 1, "col": 3, "hasRoad": false, "owner": ""}, {"row": 9, "col": 1, "hasRoad": false, "owner": ""}, {"row": 4, "col": 8, "hasRoad": false, "owner": ""}, {"row": 3, "col": 0, "hasRoad": false, "owner": ""}, {"row": 6, "col": 6, "hasRoad": false, "owner": ""}, {"row": 8, "col": 0, "hasRoad": false, "owner": ""}, {"row": 2, "col": 1, "hasRoad": false, "owner": ""}, {"row": 6, "col": 2, "hasRoad": false, "owner": ""}, {"row": 5, "col": 1, "hasRoad": false, "owner": ""}, {"row": 2, "col": 5, "hasRoad": false, "owner": ""}, {"row": 0, "col": 3, "hasRoad": false, "owner": ""}, {"row": 10, "col": 3, "hasRoad": false, "owner": ""}, {"row": 2, "col": 4, "hasRoad": false, "owner": ""}, {"row": 7, "col": 2, "hasRoad": false, "owner": ""}, {"row": 4, "col": 0, "hasRoad": false, "owner": ""}, {"row": 1, "col": 2, "hasRoad": false, "owner": ""}, {"row": 8, "col": 5, "hasRoad": false, "owner": ""}, {"row": 9, "col": 0, "hasRoad": false, "owner": ""}, {"row": 6, "col": 7, "hasRoad": false, "owner": ""}, {"row": 3, "col": 3, "hasRoad": false, "owner": ""}, {"row": 4, "col": 9, "hasRoad": false, "owner": ""}, {"row": 5, "col": 5, "hasRoad": false, "owner": ""}, {"row": 8, "col": 1, "hasRoad": false, "owner": ""}, {"row": 4, "col": 4, "hasRoad": false, "owner": ""}, {"row": 10, "col": 2, "hasRoad": false, "owner": ""}, {"row": 6, "col": 3, "hasRoad": false, "owner": ""}, {"row": 5, "col": 0, "hasRoad": false, "owner": ""}, {"row": 2, "col": 2, "hasRoad": false, "owner": ""}, {"row": 3, "col": 4, "hasRoad": false, "owner": ""}, {"row": 8, "col": 6, "hasRoad": false, "owner": ""}, {"row": 10, "col": 0, "hasRoad": false, "owner": ""}, {"row": 0, "col": 4, "hasRoad": false, "owner": ""}, {"row": 4, "col": 1, "hasRoad": false, "owner": ""}, {"row": 1, "col": 1, "hasRoad": false, "owner": ""}, {"row": 6, "col": 4, "hasRoad": false, "owner": ""}, {"row": 5, "col": 4, "hasRoad": false, "owner": ""}, {"row": 2, "col": 6, "hasRoad": false, "owner": ""}, {"row": 3, "col": 2, "hasRoad": false, "owner": ""}, {"row": 10, "col": 4, "hasRoad": false, "owner": ""}, {"row": 0, "col": 0, "hasRoad": false, "owner": ""}, {"row": 7, "col": 1, "hasRoad": false, "owner": ""}, {"row": 4, "col": 5, "hasRoad": false, "owner": ""}, {"row": 8, "col": 2, "hasRoad": false, "owner": ""}, {"row": 9, "col": 3, "hasRoad": false, "owner": ""}, {"row": 6, "col": 0, "hasRoad": false, "owner": ""}, {"row": 2, "col": 3, "hasRoad": false, "owner": ""}, {"row": 0, "col": 5, "hasRoad": false, "owner": ""}, {"row": 8, "col": 7, "hasRoad": false, "owner": ""}, {"row": 10, "col": 1, "hasRoad": false, "owner": ""}, {"row": 4, "col": 2, "hasRoad": false, "owner": ""}, {"row": 1, "col": 0, "hasRoad": false, "owner": ""}, {"row": 6, "col": 5, "hasRoad": false, "owner": ""}, {"row": 5, "col": 3, "hasRoad": false, "owner": ""}, {"row": 0, "col": 1, "hasRoad": false, "owner": ""}, {"row": 2, "col": 7, "hasRoad": false, "owner": ""}, {"row": 10, "col": 5, "hasRoad": false, "owner": ""}, {"row": 8, "col": 3, "hasRoad": false, "owner": ""}, {"row": 7, "col": 0, "hasRoad": false, "owner": ""}, {"row": 4, "col": 6, "hasRoad": false, "owner": ""}, {"row": 6, "col": 8, "hasRoad": false, "owner": ""}, {"row": 9, "col": 2, "hasRoad": false, "owner": ""}, {"row": 6, "col": 1, "hasRoad": false, "owner": ""}, {"row": 3, "col": 1, "hasRoad": false, "owner": ""}, {"row": 7, "col": 4, "hasRoad": false, "owner": ""}, {"row": 2, "col": 0, "hasRoad": false, "owner": ""}, {"row": 4, "col": 3, "hasRoad": false, "owner": ""}, {"row": 5, "col": 2, "hasRoad": false, "owner": ""}, {"row": 0, "col": 2, "hasRoad": false, "owner": ""}, {"row": 8, "col": 4, "hasRoad": false, "owner": ""}], "nodes": [{"row": 4, "col": 7, "building": "", "owner": ""}, {"row": 1, "col": 3, "building": "", "owner": ""}, {"row": 4, "col": 8, "building": "", "owner": ""}, {"row": 3, "col": 0, "building": "", "owner": ""}, {"row": 2, "col": 8, "building": "", "owner": ""}, {"row": 5, "col": 6, "building": "", "owner": ""}, {"row": 2, "col": 1, "building": "", "owner": ""}, {"row": 1, "col": 6, "building": "", "owner": ""}, {"row": 3, "col": 7, "building": "", "owner": ""}, {"row": 0, "col": 3, "building": "", "owner": ""}, {"row": 2, "col": 5, "building": "", "owner": ""}, {"row": 5, "col": 1, "building": "", "owner": ""}, {"row": 2, "col": 4, "building": "", "owner": ""}, {"row": 4, "col": 0, "building": "", "owner": ""}, {"row": 1, "col": 2, "building": "", "owner": ""}, {"row": 3, "col": 3, "building": "", "owner": ""}, {"row": 2, "col": 9, "building": "", "owner": ""}, {"row": 5, "col": 5, "building": "", "owner": ""}, {"row": 3, "col": 10, "building": "", "owner": ""}, {"row": 4, "col": 4, "building": "", "owner": ""}, {"row": 1, "col": 5, "building": "", "owner": ""}, {"row": 3, "col": 6, "building": "", "owner": ""}, {"row": 2, "col": 2, "building": "", "owner": ""}, {"row": 0, "col": 4, "building": "", "owner": ""}, {"row": 5, "col": 0, "building": "", "owner": ""}, {"row": 4, "col": 1, "building": "", "owner": ""}, {"row": 1, "col": 1, "building": "", "owner": ""}, {"row": 3, "col": 2, "building": "", "owner": ""}, {"row": 0, "col": 0, "building": "", "owner": ""}, {"row": 2, "col": 6, "building": "", "owner": ""}, {"row": 5, "col": 4, "building": "", "owner": ""}, {"row": 4, "col": 5, "building": "", "owner": ""}, {"row": 5, "col": 2, "building": "", "owner": ""}, {"row": 1, "col": 4, "building": "", "owner": ""}, {"row": 2, "col": 10, "building": "", "owner": ""}, {"row": 3, "col": 9, "building": "", "owner": ""}, {"row": 0, "col": 5, "building": "", "owner": ""}, {"row": 2, "col": 3, "building": "", "owner": ""}, {"row": 4, "col": 2, "building": "", "owner": ""}, {"row": 1, "col": 0, "building": "", "owner": ""}, {"row": 3, "col": 5, "building": "", "owner": ""}, {"row": 0, "col": 1, "building": "", "owner": ""}, {"row": 2, "col": 7, "building": "", "owner": ""}, {"row": 5, "col": 3, "building": "", "owner": ""}, {"row": 4, "col": 6, "building": "", "owner": ""}, {"row": 3, "col": 1, "building": "", "owner": ""}, {"row": 3, "col": 8, "building": "", "owner": ""}, {"row": 0, "col": 6, "building": "", "owner": ""}, {"row": 1, "col": 8, "building": "", "owner": ""}, {"row": 2, "col": 0, "building": "", "owner": ""}, {"row": 4, "col": 3, "building": "", "owner": ""}, {"row": 1, "col": 7, "building": "", "owner": ""}, {"row": 3, "col": 4, "building": "", "owner": ""}, {"row": 0, "col": 2, "building": "", "owner": ""}]}');

const canWidth = 750;
const canHeight = 750;
const numRows = 5;
const padding = 10;
const hexLen = 65;
const setRad = 13;

const hexWidth = hexLen * Math.sqrt(3);
const horizOffset = hexWidth + padding;
const vertPad = (Math.sqrt(3) * padding) / 2;
const vertOffset = (hexLen * 1.5) + vertPad;
const vco = padding / Math.sqrt(3);

const colorMap = {
    STONE: "#9c9c9c",
    SHEEP: "#8eb427",
    BRICK: "#de5e30",
    WOOD: "#20953d",
    WHEAT: "#f2ba38",
    DESERT: "#c48d52"
}
const borderColor = "#c4a060";
const portColor = "#b97c31";

function draw() {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    initBoard(ctx, testData);
}

function initBoard(ctx, data) {
    var tilesObj = initHexTiles(data.tiles);
    var bgTiles = tilesObj.bgTiles;
    var hexTiles = tilesObj.hexTiles;
    for (var i = 0; i < bgTiles.length; i++) {
        bgTiles[i].draw(ctx);
    }
    for (i = 0; i < hexTiles.length; i++) {
        hexTiles[i].draw(ctx);
    }
}

function initHexTiles(tiles) {
    const out = {
        hexTiles: [],
        bgTiles: []
    };

    const boardWidth = (numRows * hexWidth) + ((numRows + 1) * padding);
    const boardHeight = ((numRows - 1) * vertOffset) + hexLen * 2;
    const initX = ((canWidth - boardWidth) / 2) + horizOffset / 2;
    const initY = (canHeight - boardHeight) / 2;

    for (var i = 0; i < tiles.length; i++) {
        const curTile = tiles[i];
        const color = colorMap[curTile.resource];
        const initXOffset = initX + Math.abs(curTile.row - Math.floor(numRows / 2)) * (horizOffset / 2);
        const x = initXOffset + horizOffset * curTile.col;
        const y = initY + curTile.row * vertOffset;

        var hexTile = new HexTile(curTile.row, curTile.col, x, y, hexLen, color, curTile.rollNum);
        var bgTile = new HexTile(curTile.row, curTile.col, x, y - 2 * vco, hexLen + 2 * vco, borderColor, null);
        out.hexTiles.push(hexTile);
        out.bgTiles.push(bgTile);
    }

    return out;
}

function radians(degrees) {
    return degrees * Math.PI / 180;
}

class HexTile {
    constructor(row, col, x, y, len, color, rollNum) {
        this.row = row;
        this.col = col;
        this.hexCoords = [x, y];
        for (var i = 1; i < 6; i++) {
            var nx = this.hexCoords[i * 2 - 2] + len * Math.cos(radians(60 * (i - 1) + 30));
            var ny = this.hexCoords[i * 2 - 1] + len * Math.sin(radians(60 * (i - 1) + 30));
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

    draw(ctx) {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.moveTo(this.hexCoords[0], this.hexCoords[1]);
        for (var i = 1; i < 6; i++) {
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
            ctx.fillText(this.rollNum, this.numX, this.numY);
        }
    }
}
