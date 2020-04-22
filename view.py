import tkinter as tk
from math import cos, sin, sqrt, radians
from random import shuffle
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

        self.can.bind("<Button-1>", self.click)

    def click(self, evt):
        clicked = self.can.find_closest(evt.x, evt.y)[0]
        self.handle_click(self.board.hex_tiles.values(), clicked)
        self.handle_click(self.board.settles, clicked)
        self.handle_click(self.board.roads, clicked)

    def handle_click(self, tiles, clicked):
        for tile in tiles:
            if tile.can_id == clicked:
                tile.selected = True
                self.can.itemconfigure(tile.can_id, fill="#ff00ff")
            else:
                tile.selected = False
                self.can.itemconfigure(tile.can_id, fill=tile.color)


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
        self.calc_nodes()
        self.draw_ports()
        self.draw_settlments()
        self.draw_roads()

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

        # for r in range(self.num_rows):
        #     num_hexes = self.num_rows - abs(r - self.num_rows // 2)
        #     init_x_offset = init_x + abs(r - self.num_rows // 2) * (self.horiz_offset / 2)
        #
        #     for c in range(num_hexes):
        #         x = init_x_offset + self.horiz_offset * c
        #         y = init_y + r * self.vert_offset
        #
        #         bg_tile = HexTile(x, y - 2 * self.vco, self.hex_len + 2 * self.vco, self.BORDER, 0, 0, "")
        #         bg_tile.draw_hexagon(self.canvas)
        #         self.hex_tiles[(r, c)] = HexTile(x, y, self.hex_len, self.COLORS.pop(), r, c, "{}.{}".format(r, c))

        for tile in self.hex_tiles.values():
            tile.draw_hexagon(self.canvas)

    def draw_settlments(self):
        for node in self.nodes.values():
            settle = SettleTile(node.x, node.y, self.set_rad, "blue")
            self.settles.append(settle)
            settle.draw_settlement(self.canvas)

    def draw_roads(self):
        num_rows = 2 * self.num_rows + 1
        for r in range(num_rows):
            is_even = r % 2 == 0
            is_bottom_half = r > num_rows // 2
            num_cols = num_rows - abs(r - 5) if is_even else ((num_rows + 1) // 2) - abs((r // 2) - 2)

            for c in range(num_cols):
                if is_even:
                    node = self.nodes[(r // 2, (c // 2) * 2 + 1)]
                    angle = -150 + 120 * (c % 2) if is_bottom_half else 150 - 120 * (c % 2)
                    road = RoadTile(node.x, node.y, angle, self.road_len, self.padding, self.set_rad, "blue")
                else:
                    node = self.nodes[(r // 2, c * 2 + 1 if is_bottom_half else c * 2)]
                    road = RoadTile(node.x, node.y, 90, self.road_len, self.padding, self.set_rad, "blue")

                self.roads.append(road)
                road.draw_road(self.canvas)

    def calc_nodes(self):
        for nr in range(self.num_rows + 1):
            is_top_half = nr < (self.num_rows + 1) / 2
            node_cols = 2 * (self.num_rows - abs((nr - (0 if is_top_half else 1)) - self.num_rows // 2)) + 1

            for nc in range(node_cols):
                is_last = nc == node_cols - 1
                tile = self.hex_tiles[(nr if is_top_half else nr - 1, (nc // 2) - 1 if is_last else nc // 2)]
                vco_mult = -1 if is_top_half else 1
                hl_mult = 0.5 if is_top_half else 1.5

                horz_offset = ((nc + 1) % 2) * (self.horiz_offset / 2 if is_last else -self.horiz_offset / 2)
                vert_offset = (tile.leng * (vco_mult + 1)) + (self.vco * vco_mult) if nc % 2 == 1 \
                    else (tile.leng * hl_mult) + (self.vco / 2 * vco_mult)

                self.nodes[(nr, nc)] = Node(nr, nc, tile.x + horz_offset, tile.y + vert_offset)

    # def draw_numbers(self):
    #     nums = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12]
    #     shuffle(nums)
    #     for tile in self.hex_tiles.values():
    #         num = nums.pop()
    #         text_color = "red" if num == 6 or num == 8 else "black"
    #         num = NumberTile(tile.x, tile.y + self.hex_len, 2 * self.hex_len / 3, 2 * self.hex_len / 3,
    #                          "white", text_color, num)
    #         self.numbers.append(num)
    #         num.draw_number(self.canvas)

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
                 self.color, border="").draw_road(canvas)
        RoadTile(self.node2_x, self.node2_y, self.angle2, self.length, self.width, self.set_rad,
                 self.color, border="").draw_road(canvas)


class HexTile:
    def __init__(self, x, y, leng, color, row, col, roll_num):
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.leng = leng
        self.color = color
        self.roll_num = roll_num

        self.selected = False
        self.can_id = None

    def draw_hexagon(self, canvas):
        angle = 60
        coords = [self.x, self.y]
        for i in range(1, 6):
            coords.append(coords[2 * i - 2] + self.leng * cos(radians(angle * (i - 1)) + radians(30)))
            coords.append(coords[2 * i - 1] + self.leng * sin(radians(angle * (i - 1)) + radians(30)))
        self.can_id = canvas.create_polygon(*coords, fill=self.color)

        if self.roll_num is not None:
            text_color = "red" if self.roll_num == 6 or self.roll_num == 8 else "black"
            num = NumberTile(self.x, self.y + self.leng, 2 * self.leng / 3, 2 * self.leng / 3,
                             "white", text_color, self.roll_num)
            num.draw_number(canvas)


class SettleTile:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

        self.selected = False
        self.can_id = None

    def draw_settlement(self, canvas):
        bbox = (self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius)
        self.can_id = canvas.create_oval(bbox, fill=self.color)


class RoadTile:
    def __init__(self, node_x, node_y, angle, length, width, set_rad, color, border="black"):
        self.node_x = node_x
        self.node_y = node_y
        self.angle = angle
        self.length = length
        self.width = width
        self.set_rad = set_rad
        self.color = color
        self.border = border

        self.selected = False
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

        self.can_id = canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, fill=self.color, outline=self.border)


class NumberTile:
    def __init__(self, cx, cy, width, height, color, text_color, number):
        self.cx = cx
        self.cy = cy
        self.width = width
        self.height = height
        self.color = color
        self.text_color = text_color
        self.number = number

        self.selected = False
        self.can_id = None

    def draw_number(self, canvas):
        bbox = self.cx - self.width / 2, self.cy - self.height / 2, self.cx + self.width / 2, self.cy + self.height / 2
        self.can_id = canvas.create_rectangle(bbox, fill=self.color, outline="black")
        canvas.create_text(self.cx, self.cy, text=self.number, font=("Purisa", int(self.height // 2)),
                           justify="center", fill=self.text_color)


class Node:
    def __init__(self, row, col, x, y):
        self.row = row
        self.col = col
        self.x = x
        self.y = y
