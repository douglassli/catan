from math import cos, sin, radians, sqrt


class PathTile:
    def __init__(self, row, col, node_x, node_y, angle, hex_len, padding, set_rad, color, border="black", state="hidden"):
        self.row = row
        self.col = col
        self.node_x = node_x
        self.node_y = node_y
        self.angle = angle
        self.hex_len = hex_len
        self.padding = padding
        self.set_rad = set_rad
        self.color = color
        self.border = border
        self.state = state

        self.open_select = False
        self.built = False
        self.can_id = None

    def draw_road(self, canvas):
        short_len = self.padding / sqrt(3)
        start_angle = self.angle - 60

        angle = 60
        coords = [self.node_x, self.node_y]
        for i in range(1, 6):
            leng = self.hex_len if i in [2, 5] else short_len
            coords.append(coords[-2] + leng * cos(radians(angle * (i - 1)) + radians(start_angle)))
            coords.append(coords[-2] + leng * sin(radians(angle * (i - 1)) + radians(start_angle)))
        self.can_id = canvas.create_polygon(coords, fill=self.color, outline=self.border, state=self.state, tags="road")

    def start_selection(self, canvas):
        if not self.built:
            self.open_select = True
            canvas.itemconfigure(self.can_id, state="normal", fill="", outline="white", activefill="white")

    def end_selection(self, canvas):
        if self.open_select:
            self.open_select = False
            canvas.itemconfigure(self.can_id, state="hidden", fill=self.color, outline="black", activefill="")

    def build(self, canvas):
        self.open_select = False
        self.built = True
        canvas.itemconfigure(self.can_id, state="normal", fill="blue", outline="black", activefill="")
