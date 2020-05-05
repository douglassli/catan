class Path:
    def __init__(self, row, col, neighbor_nodes, neighbor_paths):
        self.row = row
        self.col = col
        self.road = False
        self.owner = None
        self.neighbor_nodes = neighbor_nodes
        self.neighbor_paths = neighbor_paths

    def as_data(self):
        return {
            "row": self.row,
            "col": self.col,
            "hasRoad": self.road,
            "owner": ""
        }

    def build_road(self, player):
        self.road = True
        self.owner = player

    def owned_by(self, player):
        return self.owner is player

    def has_owner(self):
        return self.owner is not None

    def owns_any_ngbr_node(self, pid):
        return any([ngbr_node.owned_by(pid) for ngbr_node in self.neighbor_nodes])

    def owns_any_ngbr_path(self, pid):
        return any([ngbr_path.owned_by(pid) for ngbr_path in self.neighbor_paths])
