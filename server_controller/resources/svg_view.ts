const enum Items {
    PATH = "path",
    SETTLE = "settle",
    CITY = "city",
    ROBBER = "robber"
}

function setSelecting(row: number, col: number, itemType: Items): void {
    const item: HTMLElement = getItem(row, col, itemType);
    const cl: DOMTokenList = item.classList;
    item.onclick = function() {setActive(row, col, itemType);};
    cl.add("selecting");
    cl.remove("hidden", `active_${itemType}`);
}

function setActive(row: number, col: number, itemType: Items): void {
    const item: HTMLElement = getItem(row, col, itemType);
    const cl: DOMTokenList = item.classList;
    item.onclick = null;
    cl.add(`active_${itemType}`);
    cl.remove("hidden", "selecting");
}

function getItem(row: number, col: number, itemType: Items): HTMLElement {
    return document.getElementById(`${itemType}${row}_${col}`);
}

function testSelecting() {
    setSelecting(0, 0, Items.PATH);
    setSelecting(2, 2, Items.SETTLE);
    setSelecting(3, 3, Items.CITY);
    setSelecting(0, 0, Items.ROBBER);
}
