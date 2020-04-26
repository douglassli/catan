from math import sin, cos, radians


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

    def draw(self, canvas):
        self.draw_bridge(self.node1_x, self.node1_y, self.angle1, canvas)
        self.draw_bridge(self.node2_x, self.node2_y, self.angle2, canvas)

    def draw_bridge(self, node_x, node_y, angle, canvas):
        x1 = node_x + self.set_rad * cos(radians(angle)) + (self.width / 2) * cos(radians(angle - 90))
        y1 = node_y + self.set_rad * sin(radians(angle)) + (self.width / 2) * sin(radians(angle - 90))
        x2 = x1 + self.length * cos(radians(angle))
        y2 = y1 + self.length * sin(radians(angle))
        x3 = x2 + self.width * cos(radians(angle + 90))
        y3 = y2 + self.width * sin(radians(angle + 90))
        x4 = x3 + self.length * cos(radians(angle + 180))
        y4 = y3 + self.length * sin(radians(angle + 180))

        canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, fill=self.color, tags="port")
