from path_tile import PathTile


class PortTile:
    def __init__(self, node1_x, node1_y, angle1, node2_x, node2_y, angle2, length, width, set_rad, color):
        self.node1_x = node1_x
        self.node1_y = node1_y
        self.angle1 = angle1
        self.node2_x = node2_x
        self.node2_y = node2_y
        self.angle2 = angle2
        self.length = length
        self.width = width
        self.set_rad = set_rad
        self.color = color

    def draw_port(self, canvas):
        PathTile(self.node1_x, self.node1_y, self.angle1, self.length, self.width, self.set_rad,
                 self.color, border="", state="normal").draw_road(canvas)
        PathTile(self.node2_x, self.node2_y, self.angle2, self.length, self.width, self.set_rad,
                 self.color, border="", state="normal").draw_road(canvas)