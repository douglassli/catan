from math import sqrt


class RoundTile:
    def __init__(self, row, col, x, y, radius, color):
        self.row = row
        self.col = col
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

        self.open_select = False
        self.built = False
        self.can_id = None

    def draw(self, canvas):
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

    def build(self, canvas, color):
        self.color = color
        self.open_select = False
        self.built = True
        canvas.itemconfigure(self.can_id, state="normal", fill=self.color, outline="black", activefill="")

    def clicked_on(self, evt_x, evt_y):
        return self.open_select and sqrt((evt_x - self.x) ** 2 + (evt_y - self.y) ** 2) < self.radius
