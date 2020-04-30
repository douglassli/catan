from random import randint


class CatanGame:
    def __init__(self, players, num_each_res, dev_cards, tiles, nodes, paths):
        self.players = players
        self.cur_plyr_ind = 0

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

    def change_turn(self, is_setup, reverse_turns):
        if is_setup and self.cur_plyr_ind == len(self.players) - 1 and not reverse_turns:
            return True, True
        elif reverse_turns and self.cur_plyr_ind == 0:
            return False, False
        elif reverse_turns:
            self.cur_plyr_ind -= 1
            return True, True
        else:
            self.cur_plyr_ind = (self.cur_plyr_ind + 1) % len(self.players)
            return is_setup, False

    def can_build_settle(self):
        return self.players[self.cur_plyr_ind].can_build_settle()

    def get_available_settle_nodes(self, is_setup):
        out = []
        for coord, node in self.nodes.items():
            no_ngbrs = node.no_ngbr_nodes()
            own_ngbr_road = node.owns_ngbr_path(self.cur_plyr_ind)
            if no_ngbrs and node.building is None and (is_setup or own_ngbr_road):
                out.append(coord)
        return out

    def build_settle(self, coord):
        cur_player = self.players[self.cur_plyr_ind]
        cur_player.num_settles -= 1
        self.nodes[coord].build_settle(cur_player)
        return cur_player.color

    def can_build_road(self):
        return self.players[self.cur_plyr_ind].can_build_road()

    def get_avail_paths(self):
        out = []
        for coord, path in self.paths.items():
            own_ngbr_node = path.owns_any_ngbr_node(self.cur_plyr_ind)
            own_ngbr_road = path.owns_any_ngbr_path(self.cur_plyr_ind)
            if not path.road and (own_ngbr_node or own_ngbr_road):
                out.append(coord)
        return out

    def get_setup_avail_paths(self):
        for node in self.nodes.values():
            if node.owned_by(self.cur_plyr_ind) and node.all_empty_roads():
                return [(ngbr_path.row, ngbr_path.col) for ngbr_path in node.neighbor_paths]

    def build_road(self, coord):
        cur_player = self.players[self.cur_plyr_ind]
        cur_player.num_roads -= 1
        self.paths[coord].build_road(cur_player)
        # TODO check longest road
        return cur_player.color

    def roll_dice(self):
        d1 = randint(1, 6)
        d2 = randint(1, 6)
        return d1 + d2

    def distribute_resources(self, roll_num):
        for tile in self.tiles.values():
            if tile.roll_num == roll_num:
                # TODO give players correct resources
                pass
