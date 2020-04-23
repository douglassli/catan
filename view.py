import tkinter as tk
from math import cos, sin, sqrt, radians
from resources import Resource


class Application(tk.Frame):
    def __init__(self, init_game, master=None):
        super().__init__(master)
        self.master = master
        self.BG_COLOR = "#0349fc"
        self.can = tk.Canvas(self, width=800, height=800, bg=self.BG_COLOR)
        self.can.pack()
        self.pack()

        self.hex_len = 70
        self.padding = 10
        self.board = Board(self.hex_len, self.padding, 13, self.can, 800, 800)
        self.board.draw_board(init_game)

        self.can.bind("1", lambda e: self.start_selection(self.board.settles, self.is_settle, e))
        self.can.bind("2", lambda e: self.start_selection(self.board.roads, self.is_road, e))
        self.can.focus_set()

        self.selecting = False

    def start_selection(self, tiles, check, evt):
        if self.selecting:
            return
        self.selecting = True
        for tile in tiles:
            tile.start_selection(self.can)
        self.can.bind("<Button-1>", lambda e: self.handle_selection(tiles, check, e))

    def handle_selection(self, tiles, check, evt):
        clicked = self.can.find_closest(evt.x, evt.y)[0]
        if check(clicked):
            for tile in tiles:
                if tile.can_id == clicked:
                    tile.build(self.can)
                else:
                    tile.end_selection(self.can)
            self.can.bind("<Button-1>", None)
            self.selecting = False

    def is_settle(self, cid):
        for settle in self.board.settles:
            if settle.can_id == cid:
                print("true")
                return True
        return False

    def is_road(self, cid):
        for road in self.board.roads:
            if road.can_id == cid:
                print("true")
                return True
        return False


class Board:
    def __init__(self, hex_len, padding, set_rad, canvas, can_wid, can_height):
        self.hex_len = hex_len
        self.padding = padding
        self.set_rad = set_rad
        self.canvas = canvas
        self.can_wid = can_wid
        self.can_height = can_height
        self.num_rows = 5
        self.hex_tiles = {}
        self.nodes = {}
        self.settles = []
        self.roads = []
        self.numbers = []

        self.hex_wid = self.hex_len * sqrt(3)
        self.horiz_offset = self.hex_wid + self.padding
        self.vert_pad = (sqrt(3) * self.padding) / 2
        self.vert_offset = (self.hex_len * 1.5) + self.vert_pad
        self.vco = self.padding / sqrt(3)
        self.settle_dist = self.vco + self.hex_len
        self.road_len = self.settle_dist - (2 * self.set_rad)

        self.color_map = {
            Resource.STONE: "#9c9c9c",
            Resource.SHEEP: "#8eb427",
            Resource.BRICK: "#de5e30",
            Resource.WOOD: "#20953d",
            Resource.WHEAT: "#f2ba38",
            Resource.DESERT: "#c48d52"
        }

        self.BORDER = "#c4a060"
        self.PORT = "#b97c31"

    def draw_board(self, catan_game):
        self.canvas.create_rectangle((0, 0, self.can_wid, self.can_height), fill="#0349fc")
        self.draw_tiles(catan_game.tiles)
        self.calc_nodes(catan_game.nodes)
        self.draw_ports()
        self.draw_settlments()
        self.draw_roads(catan_game.paths)

    def draw_tiles(self, tiles):
        board_width = (self.num_rows * self.hex_wid) + ((self.num_rows + 1) * self.padding)
        board_height = ((self.num_rows - 1) * self.vert_offset) + self.hex_len * 2
        init_x = ((self.can_wid - board_width) / 2) + self.horiz_offset / 2
        init_y = (self.can_height - board_height) / 2

        for tile in tiles.values():
            color = self.color_map[tile.resource]
            init_x_offset = init_x + abs(tile.row - self.num_rows // 2) * (self.horiz_offset / 2)
            x = init_x_offset + self.horiz_offset * tile.col
            y = init_y + tile.row * self.vert_offset

            HexTile(x, y - 2 * self.vco, self.hex_len + 2 * self.vco, self.BORDER, 0, 0, None).draw_hexagon(self.canvas)
            self.hex_tiles[(tile.row, tile.col)] = HexTile(x, y, self.hex_len, color, tile.row, tile.col, tile.roll_num)

        for tile in self.hex_tiles.values():
            tile.draw_hexagon(self.canvas)

    def draw_settlments(self):
        for node in self.nodes.values():
            settle = SettleTile(node.x, node.y, self.set_rad, "blue")
            self.settles.append(settle)
            settle.draw_settlement(self.canvas)

    def draw_roads(self, paths):
        num_rows = 2 * self.num_rows + 1
        for path in paths.values():
            is_even = path.row % 2 == 0
            is_bottom_half = path.row > num_rows // 2

            if is_even:
                node = self.nodes[(path.row // 2, (path.col // 2) * 2 + 1)]
                angle = -150 + 120 * (path.col % 2) if is_bottom_half else 150 - 120 * (path.col % 2)
                road = RoadTile(node.x, node.y, angle, self.road_len, self.padding, self.set_rad, "blue")
            else:
                node = self.nodes[(path.row // 2, path.col * 2 + 1 if is_bottom_half else path.col * 2)]
                road = RoadTile(node.x, node.y, 90, self.road_len, self.padding, self.set_rad, "blue")

            self.roads.append(road)
            road.draw_road(self.canvas)

    def calc_nodes(self, nodes):
        for node in nodes.values():
            is_top_half = node.row < (self.num_rows + 1) / 2
            node_cols = max([nk[1] for nk in nodes if nk[0] == node.row]) + 1

            is_last = node.col == node_cols - 1
            tile = self.hex_tiles[(node.row if is_top_half else node.row - 1,
                                   (node.col // 2) - 1 if is_last else node.col // 2)]
            vco_mult = -1 if is_top_half else 1
            hl_mult = 0.5 if is_top_half else 1.5

            horz_offset = ((node.col + 1) % 2) * (self.horiz_offset / 2 if is_last else -self.horiz_offset / 2)
            vert_offset = (tile.leng * (vco_mult + 1)) + (self.vco * vco_mult) if node.col % 2 == 1 \
                else (tile.leng * hl_mult) + (self.vco / 2 * vco_mult)

            self.nodes[(node.row, node.col)] = Node(node.row, node.col, tile.x + horz_offset,
                                                    tile.y + vert_offset, node.building)

    def draw_ports(self):
        port_poss = [(0, 0, -90, 0, 1, -150),
                     (0, 3, -30, 0, 4, -90),
                     (1, 0, 150, 2, 1, -150),
                     (1, 7, -30, 1, 8, -90),
                     (3, 1, 150, 4, 0, -150),
                     (2, 10, 30, 3, 10, -30),
                     (5, 0, 90, 5, 1, 150),
                     (5, 3, 30, 5, 4, 90),
                     (4, 7, 30, 4, 8, 90)]
        for pos in port_poss:
            n1 = self.nodes[(pos[0], pos[1])]
            n2 = self.nodes[(pos[3], pos[4])]
            port = Port(n1.x, n1.y, pos[2], n2.x, n2.y, pos[5], self.road_len, self.padding, 0, self.PORT)
            port.draw_port(self.canvas)


class Port:
    def __init__(self, node1_x, node1_y, angle1, node2_x, node2_y, angle2, length, width, set_rad, color):
        self.node1_x = node1_x
        self.node1_y = node1_y
        self.angle1 = angle1
        self.node2_x = node2_x
        self.node2_y = node2_y
        self.angle2 = angle2
        self.length = length
        self.width = width
        self.set_rad = set_rad
        self.color = color

    def draw_port(self, canvas):
        RoadTile(self.node1_x, self.node1_y, self.angle1, self.length, self.width, self.set_rad,
                 self.color, border="", state="normal").draw_road(canvas)
        RoadTile(self.node2_x, self.node2_y, self.angle2, self.length, self.width, self.set_rad,
                 self.color, border="", state="normal").draw_road(canvas)


class HexTile:
    def __init__(self, x, y, leng, color, row, col, roll_num):
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.leng = leng
        self.color = color
        self.roll_num = roll_num

        self.can_id = None

    def draw_hexagon(self, canvas):
        angle = 60
        coords = [self.x, self.y]
        for i in range(1, 6):
            coords.append(coords[2 * i - 2] + self.leng * cos(radians(angle * (i - 1)) + radians(30)))
            coords.append(coords[2 * i - 1] + self.leng * sin(radians(angle * (i - 1)) + radians(30)))
        self.can_id = canvas.create_polygon(*coords, fill=self.color, tags="hex")

        if self.roll_num is not None:
            text_color = "red" if self.roll_num == 6 or self.roll_num == 8 else "black"
            num_len = 2 * self.leng / 3
            num = NumberTile(self.x, self.y + self.leng, num_len, num_len, "white", text_color, self.roll_num)
            num.draw_number(canvas)


class SettleTile:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

        self.open_select = False
        self.built = False
        self.can_id = None

    def draw_settlement(self, canvas):
        bbox = (self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius)
        self.can_id = canvas.create_oval(bbox, fill=self.color, state="hidden", tags="settle")

    def start_selection(self, canvas):
        if not self.built:
            self.open_select = True
            canvas.itemconfigure(self.can_id, state="normal", fill="", outline="white", activefill="white")

    def end_selection(self, canvas):
        if self.open_select:
            self.open_select = False
            canvas.itemconfigure(self.can_id, state="hidden", fill=self.color, outline="black", activefill="")

    def build(self, canvas):
        self.open_select = False
        self.built = True
        canvas.itemconfigure(self.can_id, state="normal", fill="blue", outline="black", activefill="")


class RoadTile:
    def __init__(self, node_x, node_y, angle, length, width, set_rad, color, border="black", state="hidden"):
        self.node_x = node_x
        self.node_y = node_y
        self.angle = angle
        self.length = length
        self.width = width
        self.set_rad = set_rad
        self.color = color
        self.border = border
        self.state = state

        self.open_select = False
        self.built = False
        self.can_id = None

    def draw_road(self, canvas):
        x1 = self.node_x + self.set_rad * cos(radians(self.angle)) + (self.width / 2) * cos(radians(self.angle - 90))
        y1 = self.node_y + self.set_rad * sin(radians(self.angle)) + (self.width / 2) * sin(radians(self.angle - 90))
        x2 = x1 + self.length * cos(radians(self.angle))
        y2 = y1 + self.length * sin(radians(self.angle))
        x3 = x2 + self.width * cos(radians(self.angle + 90))
        y3 = y2 + self.width * sin(radians(self.angle + 90))
        x4 = x3 + self.length * cos(radians(self.angle + 180))
        y4 = y3 + self.length * sin(radians(self.angle + 180))

        self.can_id = canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4,
                                            fill=self.color, outline=self.border, state=self.state, tags="road")

    def start_selection(self, canvas):
        if not self.built:
            self.open_select = True
            canvas.itemconfigure(self.can_id, state="normal", fill="", outline="white", activefill="white")

    def end_selection(self, canvas):
        if self.open_select:
            self.open_select = False
            canvas.itemconfigure(self.can_id, state="hidden", fill=self.color, outline="black", activefill="")

    def build(self, canvas):
        self.open_select = False
        self.built = True
        canvas.itemconfigure(self.can_id, state="normal", fill="blue", outline="black", activefill="")


class NumberTile:
    def __init__(self, cx, cy, width, height, color, text_color, number):
        self.cx = cx
        self.cy = cy
        self.width = width
        self.height = height
        self.color = color
        self.text_color = text_color
        self.number = number

        self.can_id = None

    def draw_number(self, canvas):
        bbox = self.cx - self.width / 2, self.cy - self.height / 2, self.cx + self.width / 2, self.cy + self.height / 2
        self.can_id = canvas.create_rectangle(bbox, fill=self.color, outline="black")
        canvas.create_text(self.cx, self.cy, text=self.number, font=("Purisa", int(self.height // 2)),
                           justify="center", fill=self.text_color)


class Node:
    def __init__(self, row, col, x, y, building):
        self.row = row
        self.col = col
        self.x = x
        self.y = y
        self.building = building
