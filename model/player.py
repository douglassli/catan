from model.resources import Resource
from model.development_cards import DevCards


class PlayerState:
    def __init__(self, pid, name, color, resources, dev_cards, num_roads, num_settles, num_cities,
                 army_size, largest_army, longest_road, victory_points):
        self.pid = pid
        self.name = name
        self.color = color
        self.resources = resources
        self.dev_cards = dev_cards
        self.num_roads = num_roads
        self.num_settles = num_settles
        self.num_cities = num_cities
        self.army_size = army_size
        self.largest_army = largest_army
        self.longest_road = longest_road
        self.victory_points = victory_points

    def get_state(self):
        return PlayerState(self.pid, self.name, self.color,
                           {res: num for res, num in self.resources.items()},
                           {dc: num for dc, num in self.dev_cards.items()},
                           self.num_roads, self.num_settles, self.num_cities, self.army_size,
                           self.largest_army, self.longest_road, self.victory_points)


class Player(PlayerState):
    def __init__(self, pid, name, color, num_roads=15, num_settles=5, num_cities=4):
        resources = {res: 0 for res in Resource if res != Resource.DESERT}
        dev_cards = {dc: 0 for dc in DevCards}
        super().__init__(pid, name, color, resources, dev_cards, num_roads, num_settles, num_cities, 0, False, False, 0)

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

    def buy_road(self):
        self.resources[Resource.WOOD] -= 1
        self.resources[Resource.BRICK] -= 1

    def buy_settle(self):
        self.resources[Resource.WOOD] -= 1
        self.resources[Resource.BRICK] -= 1
        self.resources[Resource.SHEEP] -= 1
        self.resources[Resource.WHEAT] -= 1

    def buy_city(self):
        self.resources[Resource.WHEAT] -= 2
        self.resources[Resource.STONE] -= 3

    def buy_dev_card(self):
        self.resources[Resource.WHEAT] -= 1
        self.resources[Resource.SHEEP] -= 1
        self.resources[Resource.STONE] -= 1

    def gain_resource(self, resource, count):
        self.resources[resource] += count
