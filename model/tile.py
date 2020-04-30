class Tile:
    def __init__(self, row, col, resource, roll_num, nodes, has_robber):
        self.row = row
        self.col = col
        self.resource = resource
        self.roll_num = roll_num
        self.nodes = nodes
        self.has_robber = has_robber

    def give_resources(self, roll_num):
        if self.roll_num == roll_num:
            for node in self.nodes:
                node.give_resource(self.resource)
