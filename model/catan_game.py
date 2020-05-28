from random import randint
from model.resources import Resource
from model.buildings import Buildings
from model.ports import Port
from socket_server.game_state import GameState


class CatanGame:
    def __init__(self, players, num_each_res, dev_cards, tiles, nodes, paths, ports):
        self.players = players
        self.cur_plyr_ind = 0

        self.dev_cards = dev_cards
        self.resources = {res: num_each_res for res in Resource if res != Resource.DESERT}

        self.tiles = tiles
        self.nodes = nodes
        self.paths = paths

        self.ports = ports

    def cur_player(self):
        return self.players[self.cur_plyr_ind]

    def get_player_by_name(self, name):
        for player in self.players:
            if player.name == name:
                return player

    def get_player_by_id(self, pid):
        for player in self.players:
            if player.pid == pid:
                return player

    def change_turn(self, game_state):
        if game_state == GameState.SETUP and self.cur_plyr_ind == len(self.players) - 1:
            return GameState.SETUP_REV
        elif game_state == GameState.SETUP_REV and self.cur_plyr_ind == 0:
            return GameState.PRE_ROLL
        elif game_state == GameState.SETUP_REV:
            self.cur_plyr_ind -= 1
            return GameState.SETUP_REV
        else:
            prev_cur_player = self.cur_player()
            prev_cur_player.move_dev_cards()
            prev_cur_player.used_dev_card = False
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
        used_resources = cur_player.buy_settle(is_setup)
        self.return_to_deck(used_resources)
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
        used_resources = cur_player.buy_city(is_setup)
        self.return_to_deck(used_resources)
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
        used_resources = cur_player.buy_road(is_setup)
        self.return_to_deck(used_resources)
        self.paths[coord].build_road(cur_player)
        self.update_longest_road()
        return cur_player.color

    def build_road_dev_card(self, coord, is_setup):
        cur_player = self.cur_player()
        cur_player.num_roads -= 1
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

    def get_avail_to_rob(self, coord):
        cur_plyr = self.cur_player()
        return list(set([plyr.name for plyr in self.tiles[coord].get_avail_to_rob() if plyr.name != cur_plyr.name]))

    def can_rob(self, robbed_name):
        for tile in self.tiles.values():
            if tile.has_robber:
                return tile.can_rob(robbed_name)

    def rob_player(self, robbed_name):
        cur_plyr = self.cur_player()
        robbed_plyr = self.get_player_by_name(robbed_name)
        resource = robbed_plyr.steal_random_resource()
        cur_plyr.gain_resource(resource, 1)

    def roll_dice(self):
        d1 = randint(1, 6)
        d2 = randint(1, 6)
        return d1, d2

    def distribute_resources(self, roll_num):
        for tile in self.tiles.values():
            res, num = tile.give_resources(roll_num)
            if res != Resource.DESERT:
                self.resources[res] -= num

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
                self.resources[tile.resource] -= 1

    def return_to_deck(self, used_resources):
        for res, num in used_resources.items():
            self.resources[res] += num

    def buy_dev_card(self):
        used_resources = self.cur_player().buy_dev_card(self.dev_cards.pop())
        self.return_to_deck(used_resources)

    def can_do_trade(self, plyr1, p1_resources, plyr2, p2_resources):
        return plyr1.has_resources(p1_resources) and plyr2.has_resources(p2_resources)

    def find_avail_ports(self):
        cur_plyr = self.cur_player()
        return [node.port for node in self.nodes.values() if node.owned_by(cur_plyr) and node.port != Port.NO_PORT]

    def can_trade_with_bank(self, cur_resources, other_resources):
        avail_ports = self.find_avail_ports()
        default = 3 if Port.ANY in avail_ports else 4
        trade_rates = {
            Resource.WOOD: 2 if Port.WOOD in avail_ports else default,
            Resource.BRICK: 2 if Port.BRICK in avail_ports else default,
            Resource.SHEEP: 2 if Port.SHEEP in avail_ports else default,
            Resource.WHEAT: 2 if Port.WHEAT in avail_ports else default,
            Resource.STONE: 2 if Port.STONE in avail_ports else default
        }

        allowed_num = 0
        for res, num in cur_resources.items():
            if num % trade_rates[res] != 0:
                return False
            allowed_num += num // trade_rates[res]

        return allowed_num == sum([num for num in other_resources.values()])

    def trade_with_bank(self, cur_resources, other_resources):
        cur_plyr = self.cur_player()
        for res, num in cur_resources.items():
            cur_plyr.gain_resource(res, -num)
            self.resources[res] += num

        for res, num in other_resources.items():
            self.resources[res] -= num
            cur_plyr.gain_resource(res, num)

    def perform_trade(self, plyr1, p1_resources, plyr2, p2_resources):
        for res, val in p1_resources.items():
            plyr1.gain_resource(res, -val)
            plyr2.gain_resource(res, val)

        for res, val in p2_resources.items():
            plyr1.gain_resource(res, val)
            plyr2.gain_resource(res, -val)

    def use_knight(self):
        self.cur_player().use_knight()

        largest = 0
        prev_holder = None
        for player in self.players:
            if player.largest_army and player.army_size >= largest:
                prev_holder = player
                largest = player.army_size
            elif player.largest_army and player.army_size < largest:
                player.largest_army = False
            elif not player.largest_army and player.army_size > largest and player.army_size >= 3:
                if prev_holder is not None:
                    prev_holder.largest_army = False
                prev_holder = player
                player.largest_army = True
                largest = player.army_size

    def use_monopoly(self, res):
        cur_plyr = self.cur_player()
        cur_plyr.use_monopoly()
        for plyr in self.players:
            if plyr is not cur_plyr:
                num = plyr.steal_all_of_resource(res)
                cur_plyr.gain_resource(res, num)
