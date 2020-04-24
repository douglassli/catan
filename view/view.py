import tkinter as tk
from math import sqrt
from model.resources import Resource
from view.hex_tile import HexTile
from view.node_pos import Node
from view.path_tile import PathTile
from view.settle_tile import SettleTile
from view.port_tile import PortTile


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

        self.can.bind("1", lambda e: self.start_settle_selection())
        # self.can.bind("2", lambda e: self.start_selection(self.board.roads))
        self.can.focus_set()

        self.selecting = False
        self.controller = None

    def start_settle_selection(self):
        if self.selecting:
            return
        self.selecting = True
        self.controller.start_settle_selection()

    def display_settle_options(self, avail):
        self.board.show_settle_options(avail)
        self.can.bind("<Button-1>", lambda e: self.handle_settle_selection(e))

    def handle_settle_selection(self, evt):
        clicked = self.can.find_closest(evt.x, evt.y)[0]
        if self.board.is_id_in_settles(clicked):
            selected = self.board.build_settle(clicked)
            self.can.bind("<Button-1>", None)
            self.selecting = False
            self.controller.handle_settle_build(selected)

    def handle_selection(self, tiles, evt):
        clicked = self.can.find_closest(evt.x, evt.y)[0]
        if self.is_in_list(tiles, clicked):
            for tile in tiles:
                if tile.can_id == clicked:
                    tile.build(self.can)
                else:
                    tile.end_selection(self.can)
            self.can.bind("<Button-1>", None)
            self.selecting = False

    def is_in_list(self, items, cid):
        for item in items:
            if item.can_id == cid:
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
        self.settles = {}
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
        self.draw_roads(catan_game.paths)
        self.draw_settlments()

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
            settle = SettleTile(node.row, node.col, node.x, node.y, self.set_rad, "blue")
            self.settles[(node.row, node.col)] = settle
            settle.draw_settlement(self.canvas)

    def draw_roads(self, paths):
        num_rows = 2 * self.num_rows + 1
        for path in paths.values():
            is_even = path.row % 2 == 0
            is_bottom_half = path.row > num_rows // 2

            if is_even:
                node = self.nodes[(path.row // 2, (path.col // 2) * 2 + 1)]
                angle = -150 + 120 * (path.col % 2) if is_bottom_half else 150 - 120 * (path.col % 2)
                road = PathTile(node.x, node.y, angle, self.hex_len, self.padding, self.set_rad, "blue")
            else:
                node = self.nodes[(path.row // 2, path.col * 2 + 1 if is_bottom_half else path.col * 2)]
                road = PathTile(node.x, node.y, 90, self.hex_len, self.padding, self.set_rad, "blue")

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
            port = PortTile(n1.x, n1.y, pos[2], n2.x, n2.y, pos[5], self.road_len, self.padding, 0, self.PORT)
            port.draw_port(self.canvas)

    def is_id_in_settles(self, cid):
        for settle in self.settles.values():
            if settle.can_id == cid:
                return True
        return False

    def show_settle_options(self, avail):
        for coord in avail:
            self.settles[coord].start_selection(self.canvas)

    def build_settle(self, cid):
        out = None
        for settle in self.settles.values():
            if settle.can_id == cid:
                settle.build(self.canvas)
                out = (settle.row, settle.col)
            else:
                settle.end_selection(self.canvas)

        return out
