from model.resources import Resource
from model.development_cards import DevCards


class Player:
    def __init__(self, pid, color, num_roads=15, num_settles=5, num_cities=4):
        self.pid = pid
        self.color = color

        self.resources = {res: 0 for res in Resource}
        self.dev_cards = {dc: 0 for dc in DevCards}

        self.num_roads = num_roads
        self.num_settles = num_settles
        self.num_cities = num_cities

        self.army_size = 0
        self.largest_army = False
        self.longest_road = False
        self.victory_points = 0