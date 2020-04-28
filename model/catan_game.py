

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
        self.cur_plyr_ind = (self.cur_plyr_ind + 1) % len(self.players)

    def end_setup(self):
        self.is_setup = False

    def get_available_settle_nodes(self):
        out = []
        for coord, node in self.nodes.items():
            no_ngbrs = all([self.nodes[ngbr].building is None for ngbr in node.neighbor_nodes])
            own_ngbr_road = any([self.paths[pcrd].owner == self.cur_plyr_ind for pcrd in node.neighbor_paths])
            if no_ngbrs and node.building is None and (self.is_setup or own_ngbr_road):
                out.append(coord)
        return out

    def build_settle(self, coord):
        cur_player = self.players[self.cur_plyr_ind]
        self.nodes[coord].build_settle(cur_player)
        return cur_player.color

    def get_available_paths(self):
        out = []
        for coord, path in self.paths.items():
            own_ngbr_node = any([self.nodes[ncrd].owner == self.cur_plyr_ind for ncrd in path.neighbor_nodes])
            own_ngbr_road = any([self.paths[pcrd].owner == self.cur_plyr_ind for pcrd in path.neighbor_paths])
            if not path.road and (own_ngbr_node or own_ngbr_road):
                out.append(coord)
        return out

    def build_road(self, coord):
        cur_player = self.players[self.cur_plyr_ind]
        self.paths[coord].build_road(cur_player)
        # TODO check longest road
        return cur_player.color
