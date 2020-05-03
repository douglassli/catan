import tkinter as tk
from view.initialize_board import ViewInitializer
from view.button_bar import ButtonBar
from view.player_bar import PlayerBar


class Application(tk.Frame):
    def __init__(self, init_game, master=None):
        super().__init__(master, bg="#0349fc")
        self.master = master

        self.num_rows = 5
        self.can_wid = 800
        self.can_height = 800
        self.hex_len = 70
        self.padding = 10
        self.set_rad = 13

        self.active = False
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

        self.bar_height = 75
        self.window_height = self.can_height + self.bar_height + 10
        self.right_width = 300

        self.can = tk.Canvas(master=self, width=self.can_wid, height=self.can_height, highlightthickness=0, borderwidth=0)
        b_actions = {"Trade": lambda e: None,
                     "Buy Road": lambda e: self.start_road_selection(),
                     "Buy Settle": lambda e: self.start_settle_selection(),
                     "Buy City": lambda e: None,
                     "Buy Dev Card": lambda e: None,
                     "Roll Dice": lambda e: self.start_dice_roll(),
                     "End Turn": lambda e: self.controller.handle_turn_change()}
        self.button_bar = ButtonBar(b_actions, master=self)
        self.player_bar = PlayerBar(self.right_width, self.window_height, master=self)

        self.grid()
        self.button_bar.grid(row=1)
        self.player_bar.grid(column=1, row=0, rowspan=2, padx=5)
        self.can.grid(row=0)
        self.draw_board()
        self.can.focus_set()

    def draw_board(self):
        self.can.create_rectangle((0, 0, self.can_wid, self.can_height), fill="#0349fc")
        for tile_list in self.ports, self.bg_tiles, self.hex_tiles.values(), self.roads.values(), self.settles.values(), self.robbers.values():
            for tile in tile_list:
                tile.draw(self.can)

    def start_settle_selection(self):
        if not self.active:
            self.controller.start_settle_selection()

    def start_dice_roll(self):
        if not self.active:
            self.controller.roll_dice()

    def display_settle_options(self, avail):
        self.active = True
        self.show_options(avail, self.settles)
        self.can.bind("<Button-1>", lambda e: self.handle_selection(e, self.settles, self.controller.handle_settle_build))

    def display_robber_options(self, avail):
        self.active = True
        self.show_options(avail, self.robbers)
        self.can.bind("<Button-1>", lambda e: self.handle_selection(e, self.robbers, self.controller.handle_robber_move))

    def move_robber(self, coord):
        for robber in self.robbers.values():
            if robber.built:
                robber.hide(self.can)
        self.robbers[coord].build(self.can, "black")

    def start_road_selection(self):
        if not self.active:
            self.controller.start_road_selection()

    def display_road_options(self, avail):
        self.active = True
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
        self.active = False
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

    def update_player_info(self, player_states):
        self.player_bar.update_player_info(player_states)
