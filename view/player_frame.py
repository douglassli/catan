import tkinter as tk


class PlayerFrame(tk.Frame):
    def __init__(self, width, height, master=None):
        super().__init__(master, bg="gray", height=height, width=width, bd=4, relief=tk.RIDGE)

        self.color_label = tk.Label(master=self, bg="gray", text="Color: red")
        self.color_label.grid(row=0, column=0, sticky=tk.W)
        self.wood_label = tk.Label(master=self, bg="gray", text="Num wood: 0")
        self.wood_label.grid(row=1, column=0, sticky=tk.W)
        self.brick_label = tk.Label(master=self, bg="gray", text="Num brick: 0")
        self.brick_label.grid(row=2, column=0, sticky=tk.W)
        self.sheep_label = tk.Label(master=self, bg="gray", text="Num sheep: 0")
        self.sheep_label.grid(row=3, column=0, sticky=tk.W)
        self.wheat_label = tk.Label(master=self, bg="gray", text="Num wheat: 0")
        self.wheat_label.grid(row=4, column=0, sticky=tk.W)
        self.stone_label = tk.Label(master=self, bg="gray", text="Num stone: 0")
        self.stone_label.grid(row=5, column=0, sticky=tk.W)
        self.road_label = tk.Label(master=self, bg="gray", text="Num roads: 15")
        self.road_label.grid(row=0, column=1, sticky=tk.W)
        self.settle_label = tk.Label(master=self, bg="gray", text="Num settles: 5")
        self.settle_label.grid(row=1, column=1, sticky=tk.W)
        self.city_label = tk.Label(master=self, bg="gray", text="Num cities: 4")
        self.city_label.grid(row=2, column=1, sticky=tk.W)
        self.army_size_label = tk.Label(master=self, bg="gray", text="Army size: 0")
        self.army_size_label.grid(row=3, column=1, sticky=tk.W)
        self.road_len_label = tk.Label(master=self, bg="gray", text="Road length: 0")
        self.road_len_label.grid(row=4, column=1, sticky=tk.W)
        self.vp_label = tk.Label(master=self, bg="gray", text="VP: 0")
        self.vp_label.grid(row=5, column=1, sticky=tk.W)