
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
    const tilesObj = initHexTiles(testData.tiles);
    const bgTiles = tilesObj.bgTiles;
    const hexTiles = tilesObj.hexTiles;
    for (var bgTile of bgTiles) {
        bgTile.draw(bgCtx);
    }
    for (var hexTile of hexTiles) {
        hexTile.draw(bgCtx);
    }
    // todo: ports

    const fgCanvas: HTMLCanvasElement = document.getElementById("fgCanvas") as HTMLCanvasElement;
    const fgCtx: CanvasRenderingContext2D = fgCanvas.getContext("2d");
    const tileNodes: TileNode[] = initNodes(testData.nodes, hexTiles);
    const pathTiles: PathTile[] = initPaths(testData.paths, tileNodes);
    const settles: RoundTile[] = initSettles(tileNodes);
    // for (var pathTile of pathTiles) {
    //     pathTile.draw(fgCtx);
    // }

    // for (var settle of settles) {
    //     settle.draw(fgCtx);
    // }
}

function initPaths(paths: ModelPath[], nodes: TileNode[]): PathTile[] {
    const outPaths: PathTile[] = [];
    const numPathRows: number = numRows * 2 + 1;

    for (var path of paths) {
        const isEven: boolean = path.row % 2 === 0;
        const isBottomHalf: boolean = path.row > Math.floor(numPathRows / 2);

        if (isEven) {
            const node: TileNode = findEntry(nodes, Math.floor(path.row / 2), Math.floor(path.col / 2) * 2 + 1) as TileNode;
            const angle: number = isBottomHalf ? -150 + 120 * (path.col % 2) : 150 - 120 * (path.col % 2);
            const road: PathTile = new PathTile(path.row, path.col, node.x, node.y, angle, "blue");
            outPaths.push(road);
        } else {
            const node: TileNode = findEntry(nodes, Math.floor(path.row / 2), isBottomHalf ? path.col * 2 + 1 : path.col * 2) as TileNode;
            const road: PathTile = new PathTile(path.row, path.col, node.x, node.y, 90, "blue");
            outPaths.push(road);
        }
    }
    return outPaths;
}

function initSettles(tileNodes: TileNode[]): RoundTile[] {
    const outSettles: RoundTile[] = [];
    for (var tileNode of tileNodes) {
        const settle: RoundTile = new RoundTile(tileNode.row, tileNode.col, tileNode.x, tileNode.y, setRad, "blue");
        outSettles.push(settle);
    }
    return outSettles;
}

function initNodes(nodes: ModelNode[], hexTiles: HexTile[]): TileNode[] {
    const outNodes: TileNode[] = [];
    for (var node of nodes) {
        const isTopHalf: boolean = node.row < (numRows + 1) / 2;
        const nodeCols: number = Math.max(...nodes.map((cn) => cn.row === node.row ? cn.col : -1)) + 1;

        const isLast: boolean = node.col === nodeCols - 1;

        const tileRow: number = isTopHalf ? node.row : node.row - 1;
        const tileCol: number = isLast ? Math.floor(node.col / 2) - 1 : Math.floor(node.col / 2);
        const curTile: HexTile = findEntry(hexTiles, tileRow, tileCol) as HexTile;

        const vcoMult = isTopHalf ? -1 : 1;
        const hlMult = isTopHalf ? 0.5 : 1.5;

        const hOffset = ((node.col + 1) % 2) * ((horizOffset / 2) * (isLast ? 1 : -1));
        const vOffset = node.col % 2 === 1 ? (curTile.len * (vcoMult + 1)) + (vco * vcoMult) : (curTile.len * hlMult) + (vco / 2 * vcoMult);

        const newNode: TileNode = new TileNode(node.row, node.col, curTile.x + hOffset, curTile.y + vOffset);
        outNodes.push(newNode);
    }
    return outNodes;
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

function findEntry(list: Tile[], row: number, col: number): Tile {
    for (var entry of list) {
        if (entry.row === row && entry.col === col) {
            return entry;
        }
    }
    return null;
}

class Tile {
    row: number;
    col: number;

    constructor(row: number, col: number) {
        this.row = row;
        this.col = col;
    }
}

class TileNode extends Tile {
    x: number;
    y: number;

    constructor(row: number, col: number, x: number, y: number) {
        super(row, col);
        this.x = x;
        this.y = y;
    }
}

class RoundTile extends Tile {
    x: number;
    y: number;
    radius: number;
    color: string;

    constructor(row: number, col: number, x: number, y: number, radius: number, color: string) {
        super(row, col);
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.color = color;
    }

    draw(ctx: CanvasRenderingContext2D): void {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, 2 * Math.PI);
        ctx.fillStyle = this.color;
        ctx.fill();

        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, 2 * Math.PI);
        ctx.fillStyle = "black";
        ctx.stroke();
    }
}

class HexagonShapeTile extends Tile {
    coords: number[];
    x: number;
    y: number;
    color: string;

    constructor(row: number, col: number, coords: number[], x: number, y: number, color: string) {
        super(row, col);
        this.coords = coords;
        this.x = x;
        this.y = y;
        this.color = color;
    }

    drawHexagon(ctx: CanvasRenderingContext2D, withStroke: boolean): void {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.moveTo(this.coords[0], this.coords[1]);
        for (let i: number = 1; i < 6; i++) {
            ctx.lineTo(this.coords[i * 2], this.coords[i * 2 + 1]);
        }
        ctx.fill();
        if (withStroke) {
            ctx.stroke();
        }
    }
}

class PathTile extends HexagonShapeTile {
    constructor(row: number, col: number, x: number, y: number, angle: number, color: string) {
        const tmpCoords: number[] = [x, y];
        const startAngle: number = angle - 60;
        for (let i: number = 1; i < 6; i++) {
            const sideLen: number = i === 2 || i === 5 ? hexLen : padding / Math.sqrt(3);
            const nx: number = tmpCoords[i * 2 - 2] + sideLen * Math.cos(radians(60 * (i - 1) + startAngle));
            const ny: number = tmpCoords[i * 2 - 1] + sideLen * Math.sin(radians(60 * (i - 1) + startAngle));
            tmpCoords.push(nx);
            tmpCoords.push(ny);
        }
        super(row, col, tmpCoords, x, y, color);
    }

    draw(ctx: CanvasRenderingContext2D): void {
        this.drawHexagon(ctx, true);
    }
}

class HexTile extends HexagonShapeTile {
    len: number;
    rollNum: number;
    numTileLen: number;
    numTileX: number;
    numTileY: number;
    numColor: string;
    numX: number;
    numY: number;
    numFont: string;

    constructor(row: number, col: number, x: number, y: number, len: number, color: string, rollNum: number) {
        const tmpCoords: number[] = [x, y];
        for (let i: number = 1; i < 6; i++) {
            const nx: number = tmpCoords[i * 2 - 2] + len * Math.cos(radians(60 * (i - 1) + 30));
            const ny: number = tmpCoords[i * 2 - 1] + len * Math.sin(radians(60 * (i - 1) + 30));
            tmpCoords.push(nx);
            tmpCoords.push(ny);
        }
        super(row, col, tmpCoords, x, y, color);
        this.len = len;
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
        this.drawHexagon(ctx, false);

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
