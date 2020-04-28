class Path:
    def __init__(self, row, col, neighbor_nodes, neighbor_paths):
        self.row = row
        self.col = col
        self.road = False
        self.owner = None
        self.neighbor_nodes = neighbor_nodes
        self.neighbor_paths = neighbor_paths

    def build_road(self, player):
        self.road = True
        self.owner = player.pid
