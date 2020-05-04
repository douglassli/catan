import tkinter as tk
from model.resources import Resource


class PlayerFrame(tk.Frame):
    def __init__(self, width, height, master=None):
        super().__init__(master, bg="gray", height=height, width=width, bd=4, relief=tk.RIDGE)

        self.labels = []

        self.color_var = self.make_var("Color: ...", 0, 0)
        self.wood_var = self.make_var("Num wood: ...", 1, 0)
        self.brick_var = self.make_var("Num brick: ...", 2, 0)
        self.sheep_var = self.make_var("Num sheep: ...", 3, 0)
        self.wheat_var = self.make_var("Num wheat: ...", 4, 0)
        self.stone_var = self.make_var("Num stone: ...", 5, 0)
        self.road_var = self.make_var("Num roads: ...", 0, 1)
        self.settle_var = self.make_var("Num settles: ...", 1, 1)
        self.city_var = self.make_var("Num cities: ...", 2, 1)
        self.army_size_var = self.make_var("Army size: ...", 3, 1)
        self.road_len_var = self.make_var("Road length: ...", 4, 1)
        self.vp_var = self.make_var("VP: ...", 5, 1)

        self.color = None

    def make_var(self, text, row, col):
        var = tk.StringVar()
        var.set(text)
        label = tk.Label(master=self, bg="gray", textvariable=var)
        label.grid(row=row, column=col, sticky=tk.W)
        self.labels.append(label)
        return var

    def init_player(self, player_state):
        self.color = player_state.color
        self.update_info(player_state)

    def start_turn(self):
        self.config(bg=self.color)
        for label in self.labels:
            label.config(bg=self.color)

    def end_turn(self):
        self.config(bg="gray")
        for label in self.labels:
            label.config(bg="gray")

    def update_info(self, player_state):
        self.color_var.set("Color: {}".format(player_state.color))
        self.wood_var.set("Num wood: {}".format(player_state.resources[Resource.WOOD]))
        self.brick_var.set("Num brick: {}".format(player_state.resources[Resource.BRICK]))
        self.sheep_var.set("Num sheep: {}".format(player_state.resources[Resource.SHEEP]))
        self.wheat_var.set("Num wheat: {}".format(player_state.resources[Resource.WHEAT]))
        self.stone_var.set("Num stone: {}".format(player_state.resources[Resource.STONE]))
        self.road_var.set("Num roads: {}".format(player_state.num_roads))
        self.settle_var.set("Num settles: {}".format(player_state.num_settles))
        self.city_var.set("Num cities: {}".format(player_state.num_cities))
        # self.army_size_var.set("Army size: {}".format(player_state.color))
        # self.road_len_var.set("Road length: {}".format(player_state.color))
        # self.vp_var.set("VP: {}".format(player_state.color))
