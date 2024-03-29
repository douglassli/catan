from model.resources import Resource
from model.development_cards import DevCards
from random import choices


class Player:
    def __init__(self, pid, name, color):
        self.pid = pid
        self.name = name
        self.color = color
        self.resources = {res: 0 for res in Resource if res != Resource.DESERT}
        self.dev_cards = {dc: 0 for dc in DevCards}
        self.tmp_dev_cards = {dc: 0 for dc in DevCards}
        self.num_roads = 15
        self.num_settles = 5
        self.num_cities = 4
        self.army_size = 0
        self.largest_army = False
        self.road_length = 0
        self.longest_road = False
        self.used_dev_card = False

    def can_build_settle(self):
        has_settles = self.num_settles >= 1
        has_resources = self.has_resources({Resource.WOOD: 1, Resource.WHEAT: 1, Resource.BRICK: 1, Resource.SHEEP: 1})
        return has_settles and has_resources

    def can_build_road(self):
        has_roads = self.num_roads >= 1
        has_resources = self.has_resources({Resource.WOOD: 1, Resource.BRICK: 1})
        return has_roads and has_resources

    def can_build_city(self):
        has_cities = self.num_cities >= 1
        has_resources = self.has_resources({Resource.WHEAT: 2, Resource.STONE: 3})
        return has_cities and has_resources

    def can_buy_dev_card(self):
        has_resources = self.has_resources({Resource.WHEAT: 1, Resource.STONE: 1, Resource.SHEEP: 1})
        return has_resources

    def buy_road(self, is_setup):
        self.num_roads -= 1
        if not is_setup:
            self.resources[Resource.WOOD] -= 1
            self.resources[Resource.BRICK] -= 1
            return {Resource.WOOD: 1, Resource.BRICK: 1}
        return {}

    def buy_settle(self, is_setup):
        self.num_settles -= 1
        if not is_setup:
            self.resources[Resource.WOOD] -= 1
            self.resources[Resource.BRICK] -= 1
            self.resources[Resource.SHEEP] -= 1
            self.resources[Resource.WHEAT] -= 1
            return {Resource.WOOD: 1, Resource.BRICK: 1, Resource.SHEEP: 1, Resource.WHEAT: 1}
        return {}

    def buy_city(self, is_setup):
        self.num_settles += 1
        self.num_cities -= 1
        if not is_setup:
            self.resources[Resource.WHEAT] -= 2
            self.resources[Resource.STONE] -= 3
            return {Resource.WHEAT: 2, Resource.STONE: 3}
        return {}

    def buy_dev_card(self, dev_card):
        self.tmp_dev_cards[dev_card] += 1
        self.resources[Resource.WHEAT] -= 1
        self.resources[Resource.SHEEP] -= 1
        self.resources[Resource.STONE] -= 1
        return {Resource.WHEAT: 1, Resource.SHEEP: 1, Resource.STONE: 1}

    def move_dev_cards(self):
        for dev_card, num in self.tmp_dev_cards.items():
            self.dev_cards[dev_card] += num
        self.tmp_dev_cards = {dc: 0 for dc in DevCards}

    def gain_resource(self, resource, count):
        self.resources[resource] += count

    def get_hand_size(self):
        return sum([v for v in self.resources.values()])

    def get_dev_card_hand_size(self):
        return sum([v for v in self.dev_cards.values()]) + sum([v for v in self.tmp_dev_cards.values()])

    def get_victory_points(self):
        return (5 - self.num_settles) + \
               (2 * (4 - self.num_cities)) + \
               (2 if self.longest_road else 0) + \
               (2 if self.largest_army else 0) + \
               self.dev_cards[DevCards.VP] + self.tmp_dev_cards[DevCards.VP]

    def steal_random_resource(self):
        weights = [val for val in self.resources.values()]
        resource = choices([res for res in self.resources], weights=weights, k=1)[0]
        self.resources[resource] -= 1
        return resource

    def has_resources(self, resources):
        for res, val in resources.items():
            if self.resources[res] < val:
                return False
        return True

    def use_knight(self):
        self.army_size += 1
        self.dev_cards[DevCards.KNIGHT] -= 1
        self.used_dev_card = True

    def use_road_builder(self):
        self.dev_cards[DevCards.ROAD] -= 1
        self.used_dev_card = True

    def use_monopoly(self):
        self.dev_cards[DevCards.MONOPOLY] -= 1
        self.used_dev_card = True

    def use_plenty(self, res1, res2):
        self.dev_cards[DevCards.PLENTY] -= 1
        self.used_dev_card = True
        self.gain_resource(res1, 1)
        self.gain_resource(res2, 1)

    def can_use_dev_card(self, dev_card):
        return not self.used_dev_card and self.dev_cards[dev_card] > 0

    def steal_all_of_resource(self, res):
        num = self.resources[res]
        self.resources[res] = 0
        return num
