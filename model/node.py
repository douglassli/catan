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
        self.owner = player

    def owned_by(self, player):
        return self.owner is player

    def has_owner(self):
        return self.owner is not None

    def all_empty_roads(self):
        return all([not ngbr_path.has_owner() for ngbr_path in self.neighbor_paths])

    def no_ngbr_nodes(self):
        return all([not ngbr_node.has_owner() for ngbr_node in self.neighbor_nodes])

    def owns_ngbr_path(self, pid):
        return any([ngbr_path.owned_by(pid) for ngbr_path in self.neighbor_paths])

    def give_resource(self, resource):
        if self.building == Buildings.SETTLE:
            self.owner.gain_resource(resource, 1)
        elif self.building == Buildings.CITY:
            self.owner.gain_resource(resource, 2)
