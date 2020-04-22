class Node:
    def __init__(self, row, col, building, neighbor_nodes, neighbor_paths, port):
        self.row = row
        self.col = col
        self.building = building
        self.neighbor_nodes = neighbor_nodes
        self.neighbor_paths = neighbor_paths
        self.port = port

    def __str__(self):
        return "{:2}, {:2}, {}, {}, {}, {}".format(self.row, self.col, self.building,
                                               self.neighbor_nodes, self.neighbor_paths, self.port)
