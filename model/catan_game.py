from random import randint
from model.resources import Resource
from model.buildings import Buildings
from server_controller.game_state import GameState


class CatanGame:
    def __init__(self, players, num_each_res, dev_cards, tiles, nodes, paths):
        self.players = players
        self.cur_plyr_ind = 0

        self.dev_cards = dev_cards
        self.resources = {res: num_each_res for res in Resource if res != Resource.DESERT}

        self.tiles = tiles
        self.nodes = nodes
        self.paths = paths

    def cur_player(self):
        return self.players[self.cur_plyr_ind]

    def change_turn(self, game_state):
        if game_state == GameState.SETUP and self.cur_plyr_ind == len(self.players) - 1:
            return GameState.SETUP_REV
        elif game_state == GameState.SETUP_REV and self.cur_plyr_ind == 0:
            return GameState.PRE_ROLL
        elif game_state == GameState.SETUP_REV:
            self.cur_plyr_ind -= 1
            return GameState.SETUP_REV
        else:
            self.cur_plyr_ind = (self.cur_plyr_ind + 1) % len(self.players)
            return GameState.SETUP if game_state == GameState.SETUP else GameState.PRE_ROLL

    def can_build_settle(self):
        return self.cur_player().can_build_settle()

    def get_available_settle_nodes(self, is_setup):
        out = []
        for coord, node in self.nodes.items():
            no_ngbrs = node.no_ngbr_nodes()
            own_ngbr_road = node.owns_ngbr_path(self.cur_player())
            if no_ngbrs and node.building is None and (is_setup or own_ngbr_road):
                out.append(coord)
        return out

    def build_settle(self, coord, is_setup):
        cur_player = self.cur_player()
        cur_player.buy_settle(is_setup)
        self.nodes[coord].build_settle(cur_player)
        self.update_longest_road()
        return cur_player.color

    def can_build_city(self):
        return self.cur_player().can_build_city()

    def get_avail_cities(self, is_setup):
        out = []
        cur_player = self.cur_player()
        for coord, node in self.nodes.items():
            if node.owned_by(cur_player) and node.building == Buildings.SETTLE:
                out.append(coord)
        return out

    def build_city(self, coord, is_setup):
        cur_player = self.cur_player()
        cur_player.buy_city(is_setup)
        self.nodes[coord].build_city(cur_player)
        return cur_player.color

    def can_build_road(self):
        return self.cur_player().can_build_road()

    def get_avail_paths(self, is_setup):
        if is_setup:
            return self.get_setup_avail_paths()

        out = []
        for coord, path in self.paths.items():
            own_ngbr_node = path.owns_any_ngbr_node(self.cur_player())
            own_ngbr_road = path.owns_any_ngbr_path(self.cur_player())
            if not path.road and (own_ngbr_node or own_ngbr_road):
                out.append(coord)
        return out

    def get_setup_avail_paths(self):
        for node in self.nodes.values():
            if node.owned_by(self.cur_player()) and node.all_empty_roads():
                return [(ngbr_path.row, ngbr_path.col) for ngbr_path in node.neighbor_paths]

    def build_road(self, coord, is_setup):
        cur_player = self.cur_player()
        cur_player.buy_road(is_setup)
        self.paths[coord].build_road(cur_player)
        self.update_longest_road()
        return cur_player.color

    def get_robber_coord(self):
        for tcrd, tile in self.tiles.items():
            if tile.has_robber:
                return tcrd

    def get_avail_robber_coords(self):
        return [coord for coord, tile in self.tiles.items() if not tile.has_robber]

    def move_robber(self, coord):
        for tcrd, tile in self.tiles.items():
            tile.has_robber = tcrd == coord

    def roll_dice(self):
        d1 = randint(1, 6)
        d2 = randint(1, 6)
        return d1 + d2

    def distribute_resources(self, roll_num):
        for tile in self.tiles.values():
            tile.give_resources(roll_num)

    def update_longest_road(self):
        longest = 0
        prev_holder = None
        for player in self.players:
            owned_roads = [path for path in self.paths.values() if path.owned_by(player)]
            if len(owned_roads) == 0:
                continue

            length = max([path.longest_road_from_start() for path in self.paths.values() if path.owned_by(player)])
            player.road_length = length

            if player.longest_road and length >= longest:
                prev_holder = player
                longest = length
            elif player.longest_road and length < longest:
                player.longest_road = False
            elif not player.longest_road and length > longest and length >= 5:
                if prev_holder is not None:
                    prev_holder.longest_road = False
                prev_holder = player
                player.longest_road = True
                longest = length

    def give_setup_resources(self, coord):
        plyr = self.cur_player()
        for tile in self.tiles.values():
            if tile.resource != Resource.DESERT and tile.has_node(coord):
                plyr.gain_resource(tile.resource, 1)
