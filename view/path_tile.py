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

        self.coords = []

        self.open_select = False
        self.built = False
        self.can_id = None

    def draw(self, canvas):
        short_len = self.padding / sqrt(3)
        start_angle = self.angle - 60

        angle = 60
        self.coords = [self.node_x, self.node_y]
        for i in range(1, 6):
            leng = self.hex_len if i in [2, 5] else short_len
            x = self.coords[-2] + leng * cos(radians(angle * (i - 1)) + radians(start_angle))
            y = self.coords[-1] + leng * sin(radians(angle * (i - 1)) + radians(start_angle))
            self.coords.append(x)
            self.coords.append(y)
        self.can_id = canvas.create_polygon(self.coords, fill=self.color, outline=self.border, state=self.state, tags="road")

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
        num_crossed = 0
        x1 = evt_x
        y1 = evt_y
        x2 = evt_x + 100
        y2 = evt_y
        for i in range(0, 10, 2):
            x3 = self.coords[i]
            y3 = self.coords[i + 1]
            x4 = self.coords[i + 2]
            y4 = self.coords[i + 3]

            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            tnom = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
            unom = -1 * ((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3))

            t = tnom / den
            u = unom / den

            if 0 <= t <= 1 and 0 <= u <= 1:
                num_crossed += 1

        return self.open_select and num_crossed == 1
