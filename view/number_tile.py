class NumberTile:
    def __init__(self, cx, cy, width, height, color, text_color, number):
        self.cx = cx
        self.cy = cy
        self.width = width
        self.height = height
        self.color = color
        self.text_color = text_color
        self.number = number

        self.can_id = None

    def draw_number(self, canvas):
        bbox = self.cx - self.width / 2, self.cy - self.height / 2, self.cx + self.width / 2, self.cy + self.height / 2
        self.can_id = canvas.create_rectangle(bbox, fill=self.color, outline="black")
        canvas.create_text(self.cx, self.cy, text=self.number, font=("Purisa", int(self.height // 2)),
                           justify="center", fill=self.text_color)
