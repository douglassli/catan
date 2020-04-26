import tkinter as tk
from view.initialize_board import ViewInitializer


class Application(tk.Frame):
    def __init__(self, init_game, master=None):
        super().__init__(master)
        self.master = master

        self.num_rows = 5
        self.can_wid = 800
        self.can_height = 800
        self.hex_len = 70
        self.padding = 10
        self.set_rad = 13

        self.selecting = False
        self.controller = None

        initializer = ViewInitializer(self.can_wid, self.can_height, init_game, self.num_rows,
                                      self.padding, self.hex_len, self.set_rad)
        self.hex_tiles = initializer.hex_tiles
        self.bg_tiles = initializer.bg_tiles
        self.nodes = initializer.nodes
        self.settles = initializer.settles
        self.roads = initializer.roads
        self.ports = initializer.ports

        self.can = tk.Canvas(self, width=self.can_wid, height=self.can_height)

        self.initialize()

    def initialize(self):
        self.can.pack()
        self.pack()

        self.draw_board()

        self.can.bind("1", lambda e: self.start_settle_selection())
        self.can.bind("2", lambda e: self.start_road_selection())
        self.can.focus_set()

    def draw_board(self):
        self.can.create_rectangle((0, 0, self.can_wid, self.can_height), fill="#0349fc")
        for port in self.ports:
            port.draw_port(self.can)

        for bg_tile in self.bg_tiles:
            bg_tile.draw_hexagon(self.can)

        for hex_tile in self.hex_tiles.values():
            hex_tile.draw_hexagon(self.can)

        for road in self.roads.values():
            road.draw_road(self.can)

        for settle in self.settles.values():
            settle.draw_settlement(self.can)

    def start_settle_selection(self):
        if self.selecting:
            return
        self.selecting = True
        self.controller.start_settle_selection()

    def display_settle_options(self, avail):
        self.show_options(avail, self.settles)
        self.can.bind("<Button-1>", lambda e: self.handle_selection(e, self.settles,
                                                                    self.controller.handle_settle_build))

    def start_road_selection(self):
        if self.selecting:
            return
        self.selecting = True
        self.controller.start_road_selection()

    def display_road_options(self, avail):
        self.show_options(avail, self.roads)
        self.can.bind("<Button-1>", lambda e: self.handle_selection(e, self.roads,
                                                                    self.controller.handle_road_build))

    def handle_selection(self, evt, tiles, control_handler):
        clicked = self.can.find_closest(evt.x, evt.y)[0]
        selected = self.get_from_cid(clicked, tiles)
        if selected is not None:
            selected.build(self.can)
            self.can.bind("<Button-1>", None)
            self.selecting = False
            self.end_selection()
            control_handler((selected.row, selected.col))

    def get_from_cid(self, cid, tiles):
        for tile in tiles.values():
            if tile.can_id == cid:
                return tile
        return None

    def show_options(self, avail, tiles):
        for coord in avail:
            tiles[coord].start_selection(self.can)

    def end_selection(self):
        for settle in self.settles.values():
            settle.end_selection(self.can)
        for road in self.roads.values():
            road.end_selection(self.can)
