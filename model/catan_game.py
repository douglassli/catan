

class CatanGame:
    def __init__(self, players, num_each_res, dev_cards, tiles, nodes, paths, is_setup=True):
        self.players = players
        self.cur_player = 0
        self.is_setup = is_setup

        self.dev_cards = dev_cards

        self.num_wood = num_each_res
        self.num_sheep = num_each_res
        self.num_stone = num_each_res
        self.num_wheat = num_each_res
        self.num_brick = num_each_res

        self.tiles = tiles
        self.nodes = nodes
        self.paths = paths

    def __str__(self):
        out = ""
        for nk in sorted(self.nodes):
            out += str(self.nodes[nk]) + "\n"
        return out

    def get_available_nodes(self):
        out = []
        for coord, node in self.nodes.items():
            no_ngbrs = all([self.nodes[ngbr].building is None for ngbr in node.neighbor_nodes])
            if no_ngbrs:
                out.append(coord)
        return out

    def build_settle(self, node):
        self.nodes[node].build_settle(self.cur_player)
