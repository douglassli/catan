class Tile:
    def __init__(self, row, col, resource, roll_num, nodes, has_robber):
        self.row = row
        self.col = col
        self.resource = resource
        self.roll_num = roll_num
        self.nodes = nodes
        self.has_robber = has_robber
