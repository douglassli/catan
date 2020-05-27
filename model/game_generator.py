from random import shuffle
from model.resources import Resource
from model.tile import Tile
from model.node import Node
from model.path import Path
from model.development_cards import DevCards
from model.catan_game import CatanGame
from model.player import Player
from model.ports import Port


def generate_catan_game(plyrs, num_rows=5):
    players = generate_players(plyrs)

    dev_cards = [DevCards.KNIGHT] * 14 + [DevCards.VP] * 5 + [DevCards.ROAD, DevCards.MONOPOLY, DevCards.PLENTY] * 2
    shuffle(dev_cards)

    port_nodes, ports = generate_port_assignments()

    tiles = generate_tiles(num_rows)
    nodes = generate_nodes(num_rows, tiles, port_nodes)
    paths = generate_paths(nodes)

    for tile in tiles.values():
        tile.nodes = [nodes[ncrd] for ncrd in tile.nodes]

    for node in nodes.values():
        node.neighbor_nodes = [nodes[ncrd] for ncrd in node.neighbor_nodes]
        node.neighbor_paths = [paths[pcrd] for pcrd in node.neighbor_paths]

    for path in paths.values():
        path.neighbor_nodes = [nodes[ncrd] for ncrd in path.neighbor_nodes]
        path.neighbor_paths = [paths[pcrd] for pcrd in path.neighbor_paths]

    return CatanGame(players, 19, dev_cards, tiles, nodes, paths, ports)


def generate_players(players):
    return [Player(plyr["pid"], plyr["name"], plyr["color"]) for plyr in players]


def generate_tiles(num_rows):
    # TODO make sure 6s and 8s are not next to each other
    resources = [Resource.WOOD] * 4 + [Resource.SHEEP] * 4 + [Resource.STONE] * 3 + \
                  [Resource.WHEAT] * 4 + [Resource.BRICK] * 3 + [Resource.DESERT]
    roll_nums = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
    shuffle(resources)
    shuffle(roll_nums)
    out = {}

    for r in range(num_rows):
        num_hexes = num_rows - abs(r - num_rows // 2)
        for c in range(num_hexes):
            resource = resources.pop()
            is_desert = resource == Resource.DESERT
            roll_num = None if is_desert else roll_nums.pop()
            nodes = get_tile_node_neighbors(r, c, num_rows)
            out[(r, c)] = Tile(r, c, resource, roll_num, nodes, is_desert)

    return out


def get_tile_node_neighbors(row, col, num_rows):
    cs = col * 2
    out = [(row, cs + 1), (row, cs + 2), (row + 1, cs + 1), (row + 1, cs + 2)]
    out += [(row, cs if row <= num_rows // 2 else cs + 3)]
    out += [(row + 1, cs if row >= num_rows // 2 else cs + 3)]

    return out


def generate_port_assignments():
    port_vals = [Port.WOOD, Port.BRICK, Port.SHEEP, Port.WHEAT, Port.STONE] + [Port.ANY] * 4
    shuffle(port_vals)
    # Hard coded port positions for a 5 row board. Tuples are of the form:
    # (node1_row, node1_col, node2_row, node2_col, port_num)
    # port num is counted from 0 starting at top left port and moving clockwise
    port_pairs = [(0, 0, 0, 1, 0), (0, 3, 0, 4, 1), (1, 0, 2, 1, 8), (1, 7, 1, 8, 2), (2, 10, 3, 10, 3),
                  (3, 1, 4, 0, 7), (4, 7, 4, 8, 4), (5, 0, 5, 1, 6), (5, 3, 5, 4, 5)]
    port_nodes = {}
    ports = {}
    for port_pair in port_pairs:
        port_val = port_vals.pop()
        port_nodes[(port_pair[0], port_pair[1])] = port_val
        port_nodes[(port_pair[2], port_pair[3])] = port_val

        ports[port_pair[4]] = port_val

    return port_nodes, ports


def generate_nodes(num_rows, tiles, port_assignments):
    node_coords = set([node for tile in tiles.values() for node in tile.nodes])
    out = {}
    for r, c in node_coords:
        neighbor_nodes = get_node_node_neighbors(r, c, num_rows)
        neighbor_paths = get_node_path_neighbors(r, c, num_rows)
        port = port_assignments.get((r, c), Port.NO_PORT)
        out[(r, c)] = Node(r, c, neighbor_nodes, neighbor_paths, port)

    return out


def get_node_node_neighbors(row, col, num_rows):
    is_middle = abs(row - num_rows / 2) < 1
    is_th = row < num_rows / 2
    neighbors = [(row, col - 1), (row, col + 1)]

    is_up = col % 2 == (1 if is_th else 0)
    new_row = row + (-1 if is_up else 1)

    if col % 2 == 1:
        neighbors.append((new_row, col - 1))
    elif is_middle:
        neighbors.append((new_row, col))
    else:
        neighbors.append((new_row, col + 1))

    out = []
    for coord in neighbors:
        max_col = 2 * (num_rows - abs((coord[0] - (0 if coord[0] < (num_rows + 1) / 2 else 1)) - num_rows // 2)) + 1
        if 0 <= coord[0] < num_rows + 1 and 0 <= coord[1] < max_col:
            out.append(coord)

    return out


def get_node_path_neighbors(row, col, num_rows):
    road_rows = 2 * num_rows + 1
    is_up = col % 2 == (1 if row < num_rows / 2 else 0)
    new_row = 2 * row + (-1 if is_up else 1)

    neighbors = [(2 * row, col - 1), (2 * row, col), (new_row, col // 2)]

    out = []
    for coord in neighbors:
        is_even = coord[0] % 2 == 0
        max_cols = road_rows - abs(coord[0] - 5) if is_even else ((road_rows + 1) // 2) - abs((coord[0] // 2) - 2)
        if 0 <= coord[0] < num_rows * 2 + 1 and 0 <= coord[1] < max_cols:
            out.append(coord)

    return out


def generate_paths(nodes):
    path_coords = set([crd for node in nodes.values() for crd in node.neighbor_paths])
    out = {}
    for r, c in path_coords:
        neighbor_nodes = [crd for crd in nodes if (r, c) in nodes[crd].neighbor_paths]
        neighbor_paths = [pcrd for ncrd in neighbor_nodes for pcrd in nodes[ncrd].neighbor_paths if (r, c) != pcrd]
        out[(r, c)] = Path(r, c, neighbor_nodes, neighbor_paths)

    return out
