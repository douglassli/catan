from math import sqrt
from model.resources import Resource
from view.hex_tile import HexTile
from view.node_pos import Node
from view.path_tile import PathTile
from view.round_tile import RoundTile
from view.port_tile import PortTile


class ViewInitializer:
    def __init__(self, can_wid, can_height, init_game, num_rows, padding, hex_len, set_rad):
        self.can_wid = can_wid
        self.can_height = can_height
        self.init_game = init_game
        self.num_rows = num_rows
        self.padding = padding
        self.hex_len = hex_len
        self.set_rad = set_rad

        self.hex_wid = self.hex_len * sqrt(3)
        self.horiz_offset = self.hex_wid + self.padding
        self.vert_pad = (sqrt(3) * self.padding) / 2
        self.vert_offset = (self.hex_len * 1.5) + self.vert_pad
        self.vco = self.padding / sqrt(3)

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

        self.hex_tiles, self.bg_tiles = self.init_hex_tiles(self.init_game.tiles)
        self.robber_tiles = self.init_robbers()
        self.nodes = self.init_nodes(self.init_game.nodes)
        self.settles = self.init_settlments()
        self.roads = self.init_roads(self.init_game.paths)
        self.ports = self.init_ports()

    def init_nodes(self, nodes):
        out_nodes = {}
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

            out_nodes[(node.row, node.col)] = Node(node.row, node.col, tile.x + horz_offset,
                                                   tile.y + vert_offset, node.building)

        return out_nodes

    def init_hex_tiles(self, tiles):
        bg_tiles = []
        hex_tiles = {}

        board_width = (self.num_rows * self.hex_wid) + ((self.num_rows + 1) * self.padding)
        board_height = ((self.num_rows - 1) * self.vert_offset) + self.hex_len * 2
        init_x = ((self.can_wid - board_width) / 2) + self.horiz_offset / 2
        init_y = (self.can_height - board_height) / 2

        for tile in tiles.values():
            color = self.color_map[tile.resource]
            init_x_offset = init_x + abs(tile.row - self.num_rows // 2) * (self.horiz_offset / 2)
            x = init_x_offset + self.horiz_offset * tile.col
            y = init_y + tile.row * self.vert_offset

            bg_tiles.append(HexTile(x, y - 2 * self.vco, self.hex_len + 2 * self.vco, self.BORDER, 0, 0, None))
            hex_tiles[(tile.row, tile.col)] = HexTile(x, y, self.hex_len, color, tile.row, tile.col, tile.roll_num)

        return hex_tiles, bg_tiles

    def init_robbers(self):
        robbers = {}
        for hex_tile in self.hex_tiles.values():
            r = hex_tile.row
            c = hex_tile.col
            robbers[(r, c)] = RoundTile(r, c, hex_tile.x, hex_tile.y + self.hex_len * 1.65, self.set_rad, "black")
        return robbers

    def init_settlments(self):
        settles = {}
        for node in self.nodes.values():
            settle = RoundTile(node.row, node.col, node.x, node.y, self.set_rad, "blue")
            settles[(node.row, node.col)] = settle
        return settles

    def init_roads(self, paths):
        out_paths = {}
        num_rows = 2 * self.num_rows + 1
        for path in paths.values():
            is_even = path.row % 2 == 0
            is_bottom_half = path.row > num_rows // 2

            if is_even:
                node = self.nodes[(path.row // 2, (path.col // 2) * 2 + 1)]
                angle = -150 + 120 * (path.col % 2) if is_bottom_half else 150 - 120 * (path.col % 2)
                road = PathTile(path.row, path.col, node.x, node.y, angle, self.hex_len, self.padding, self.set_rad, "blue")
            else:
                node = self.nodes[(path.row // 2, path.col * 2 + 1 if is_bottom_half else path.col * 2)]
                road = PathTile(path.row, path.col, node.x, node.y, 90, self.hex_len, self.padding, self.set_rad, "blue")

            out_paths[(path.row, path.col)] = road

        return out_paths

    def init_ports(self):
        # TODO move port calculation into model
        out_ports = []
        road_len = self.vco + self.hex_len - (2 * self.set_rad)
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
            out_ports.append(PortTile(n1.x, n1.y, pos[2], n2.x, n2.y, pos[5], road_len, self.padding, 0, self.PORT))

        return out_ports
