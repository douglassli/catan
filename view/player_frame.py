import tkinter as tk


class PlayerFrame(tk.Frame):
    def __init__(self, width, height, master=None):
        super().__init__(master, bg="gray", height=height, width=width, bd=4, relief=tk.RIDGE)

        self.color_label = self.make_label("Color: red", 0, 0)
        self.wood_label = self.make_label("Num wood: 0", 1, 0)
        self.brick_label = self.make_label("Num brick: 0", 2, 0)
        self.sheep_label = self.make_label("Num sheep: 0", 3, 0)
        self.wheat_label = self.make_label("Num wheat: 0", 4, 0)
        self.stone_label = self.make_label("Num stone: 0", 5, 0)
        self.road_label = self.make_label("Num roads: 15", 0, 1)
        self.settle_label = self.make_label("Num settles: 5", 1, 1)
        self.city_label = self.make_label("Num cities: 4", 2, 1)
        self.army_size_label = self.make_label("Army size: 0", 3, 1)
        self.road_len_label = self.make_label("Road length: 0", 4, 1)
        self.vp_label = self.make_label("VP: 0", 5, 1)

    def make_label(self, text, row, col):
        label = tk.Label(master=self, bg="gray", text=text)
        label.grid(row=row, column=col, sticky=tk.W)
        return label
