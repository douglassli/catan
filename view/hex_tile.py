from math import cos, sin, radians
from view.number_tile import NumberTile


class HexTile:
    def __init__(self, x, y, leng, color, row, col, roll_num):
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.leng = leng
        self.color = color
        self.roll_num = roll_num

        self.can_id = None

    def draw(self, canvas):
        angle = 60
        coords = [self.x, self.y]
        for i in range(1, 6):
            coords.append(coords[-2] + self.leng * cos(radians(angle * (i - 1) + 30)))
            coords.append(coords[-2] + self.leng * sin(radians(angle * (i - 1) + 30)))
        self.can_id = canvas.create_polygon(*coords, fill=self.color, tags="hex")

        if self.roll_num is not None:
            text_color = "red" if self.roll_num == 6 or self.roll_num == 8 else "black"
            num_len = 2 * self.leng / 3
            num = NumberTile(self.x, self.y + self.leng, num_len, num_len, "white", text_color, self.roll_num)
            num.draw(canvas)
