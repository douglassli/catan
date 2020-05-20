class Tile:
    def __init__(self, row, col, resource, roll_num, nodes, has_robber):
        self.row = row
        self.col = col
        self.resource = resource
        self.roll_num = roll_num
        self.nodes = nodes
        self.has_robber = has_robber

    def give_resources(self, roll_num):
        num_given = 0
        if self.roll_num == roll_num and not self.has_robber:
            for node in self.nodes:
                num_given += node.give_resource(self.resource)
        return self.resource, num_given

    def has_node(self, coord):
        for node in self.nodes:
            if node.row == coord[0] and node.col == coord[1]:
                return True
        return False
