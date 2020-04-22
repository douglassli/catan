class Node:
    def __init__(self, row, col, building, neighbor_nodes, neighbor_paths, port):
        self.row = row
        self.col = col
        self.building = building
        self.neighbor_nodes = neighbor_nodes
        self.neighbor_paths = neighbor_paths
        self.port = port
