from model.buildings import Buildings


class Node:
    def __init__(self, row, col, neighbor_nodes, neighbor_paths, port):
        self.row = row
        self.col = col
        self.building = None
        self.owner = None
        self.neighbor_nodes = neighbor_nodes
        self.neighbor_paths = neighbor_paths
        self.port = port

    def __str__(self):
        return "{:2}, {:2}, {}, {}, {}, {}".format(self.row, self.col, self.building,
                                                   self.neighbor_nodes, self.neighbor_paths, self.port)

    def build_settle(self, player):
        self.building = Buildings.SETTLE
        self.owner = player.pid
