class Path:
    def __init__(self, row, col, road, neighbor_nodes, neighbor_paths):
        self.row = row
        self.col = col
        self.road = road
        self.neighbor_nodes = neighbor_nodes
        self.neighbor_paths = neighbor_paths
