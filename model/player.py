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
        self.num_roads = 15
        self.num_settles = 5
        self.num_cities = 4
        self.army_size = 0
        self.largest_army = False
        self.road_length = 0
        self.longest_road = False

    def can_build_settle(self):
        has_settles = self.num_settles >= 1
        has_resources = self.resources[Resource.WOOD] >= 1 and self.resources[Resource.WHEAT] >= 1 and \
                        self.resources[Resource.BRICK] >= 1 and self.resources[Resource.SHEEP] >= 1
        return has_settles and has_resources

    def can_build_road(self):
        has_roads = self.num_roads >= 1
        has_resources = self.resources[Resource.WOOD] >= 1 and self.resources[Resource.BRICK] >= 1
        return has_roads and has_resources

    def can_build_city(self):
        has_cities = self.num_cities >= 1
        has_resources = self.resources[Resource.WHEAT] >= 2 and self.resources[Resource.STONE] >= 3
        return has_cities and has_resources

    def can_buy_dev_card(self):
        has_resources = self.resources[Resource.WHEAT] >= 1 and self.resources[Resource.STONE] >= 1 and \
                        self.resources[Resource.SHEEP] >= 1
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
        self.dev_cards[dev_card] += 1
        self.resources[Resource.WHEAT] -= 1
        self.resources[Resource.SHEEP] -= 1
        self.resources[Resource.STONE] -= 1
        return {Resource.WHEAT: 1, Resource.SHEEP: 1, Resource.STONE: 1}

    def gain_resource(self, resource, count):
        self.resources[resource] += count

    def get_hand_size(self):
        return sum([v for v in self.resources.values()])

    def get_dev_card_hand_size(self):
        return sum([v for v in self.dev_cards.values()])

    def get_victory_points(self):
        return (5 - self.num_settles) + \
               (2 * (4 - self.num_cities)) + \
               (2 if self.longest_road else 0) + \
               (2 if self.largest_army else 0) + \
               self.dev_cards[DevCards.VP]

    def steal_random_resource(self):
        weights = [val for val in self.resources.values()]
        resource = choices([res for res in self.resources], weights=weights, k=1)[0]
        self.resources[resource] -= 1
        return resource
