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
        self.owner = player

    def owned_by(self, player):
        return self.owner is player

    def has_owner(self):
        return self.owner is not None

    def owns_any_ngbr_node(self, plyr):
        return any([ngbr_node.owned_by(plyr) for ngbr_node in self.neighbor_nodes])

    def owns_any_ngbr_path(self, plyr):
        return len(self.get_next_owned_roads(plyr)) > 0

    def get_next_owned_roads(self, plyr):
        accessible_roads = []
        for node in self.neighbor_nodes:
            if not node.has_owner() or node.owned_by(plyr):
                accessible_roads += [path for path in node.neighbor_paths if path is not self and path.owned_by(plyr)]
        return accessible_roads

    def longest_road_from_start(self):
        longest = 1
        frontier = [(p, 1, {(self.row, self.col)}) for p in self.get_next_owned_roads(self.owner)]

        while len(frontier) > 0:
            cpath, clen, cseen = frontier.pop(0)
            longest = max(longest, clen + 1)
            for p in cpath.get_next_owned_roads(cpath.owner):
                if (p.row, p.col) not in cseen:
                    frontier.append((p, clen + 1, cseen | {(cpath.row, cpath.col)}))

        return longest
