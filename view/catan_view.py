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
        self.robbers = initializer.robber_tiles
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
        self.can.bind("3", lambda e: self.controller.handle_turn_change())
        self.can.bind("4", lambda e: self.controller.roll_dice())
        self.can.focus_set()

    def draw_board(self):
        self.can.create_rectangle((0, 0, self.can_wid, self.can_height), fill="#0349fc")
        for tile_list in self.ports, self.bg_tiles, self.hex_tiles.values(), self.roads.values(), self.settles.values(), self.robbers.values():
            for tile in tile_list:
                tile.draw(self.can)

    def start_settle_selection(self):
        if not self.selecting:
            self.controller.start_settle_selection()

    def display_settle_options(self, avail):
        self.selecting = True
        self.show_options(avail, self.settles)
        self.can.bind("<Button-1>", lambda e: self.handle_selection(e, self.settles, self.controller.handle_settle_build))

    def display_robber_options(self, avail):
        self.selecting = True
        self.show_options(avail, self.robbers)
        self.can.bind("<Button-1>", lambda e: self.handle_selection(e, self.robbers, self.controller.handle_robber_move))

    def move_robber(self, coord):
        self.robbers[coord].build(self.can, "black")

    def start_road_selection(self):
        if not self.selecting:
            self.controller.start_road_selection()

    def display_road_options(self, avail):
        self.selecting = True
        self.show_options(avail, self.roads)
        self.can.bind("<Button-1>", lambda e: self.handle_selection(e, self.roads, self.controller.handle_road_build))

    def handle_selection(self, evt, tiles, control_handler):
        for tile in tiles.values():
            if tile.clicked_on(evt.x, evt.y):
                self.end_selection()
                control_handler((tile.row, tile.col))
                return

    def build_settle(self, coord, color):
        self.settles[coord].build(self.can, color)

    def build_road(self, coord, color):
        self.roads[coord].build(self.can, color)

    def get_from_cid(self, cid, tiles):
        for tile in tiles.values():
            if tile.can_id == cid:
                return tile
        return None

    def show_options(self, avail, tiles):
        if len(avail) == 0:
            self.end_selection()
        else:
            for coord in avail:
                tiles[coord].start_selection(self.can)

    def end_selection(self):
        self.can.bind("<Button-1>", lambda e: None)
        self.selecting = False
        for settle in self.settles.values():
            settle.end_selection(self.can)
        for road in self.roads.values():
            road.end_selection(self.can)
        for robber in self.robbers.values():
            robber.end_selection(self.can)

    def cannot_build_settle(self):
        # TODO add alert to UI
        print("Cannot build settle")

    def cannot_build_road(self):
        # TODO add alert to UI
        print("Cannot build road")
