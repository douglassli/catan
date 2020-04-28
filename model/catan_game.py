

class CatanGame:
    def __init__(self, players, num_each_res, dev_cards, tiles, nodes, paths, is_setup=True):
        self.players = players
        self.cur_plyr_ind = 0
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

    def change_turn(self):
        self.cur_plyr_ind = self.cur_plyr_ind + 1 % len(self.players)

    def get_available_nodes(self):
        # TODO add additional logic for when not in game setup mode
        out = []
        for coord, node in self.nodes.items():
            no_ngbrs = all([self.nodes[ngbr].building is None for ngbr in node.neighbor_nodes])
            if no_ngbrs and node.building is None:
                out.append(coord)
        return out

    def build_settle(self, coord):
        self.nodes[coord].build_settle(self.players[self.cur_plyr_ind])

    def get_available_paths(self):
        # TODO add logic for limiting where roads may be built
        return [coord for coord, path in self.paths.items() if path.road is False]

    def build_road(self, coord):
        self.paths[coord].build_road(self.players[self.cur_plyr_ind])
        # TODO check longest road
