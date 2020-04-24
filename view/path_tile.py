from math import cos, sin, radians


class PathTile:
    def __init__(self, node_x, node_y, angle, length, width, set_rad, color, border="black", state="hidden"):
        self.node_x = node_x
        self.node_y = node_y
        self.angle = angle
        self.length = length
        self.width = width
        self.set_rad = set_rad
        self.color = color
        self.border = border
        self.state = state

        self.open_select = False
        self.built = False
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

        self.can_id = canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4,
                                            fill=self.color, outline=self.border, state=self.state, tags="road")

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
