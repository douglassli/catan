from jinja2 import Environment, PackageLoader, select_autoescape
from model.resources import Resource


def get_template_data(game):
    resource_map = {
        Resource.STONE: "#stoneTile",
        Resource.SHEEP: "#sheepTile",
        Resource.BRICK: "#brickTile",
        Resource.WOOD: "#woodTile",
        Resource.WHEAT: "#wheatTile",
        Resource.DESERT: "#desertTile"
    }

    template_data = {}
    for tile in game.tiles.values():
        template_data["tile{}_{}".format(tile.row, tile.col)] = resource_map[tile.resource]
        template_data["num{}_{}".format(tile.row, tile.col)] = "#num{}".format(tile.roll_num)

    template_data["players"] = [{"name": plyr.name, "color": plyr.color} for plyr in game.players]

    return template_data


def create_env():
    return Environment(loader=PackageLoader('http_server', 'templates'),
                       autoescape=select_autoescape(['html', 'xml']))


def fill_template(template_env, template_name, template_data):
    template = template_env.get_template(template_name)
    return template.render(template_data)


def create_page(game=None):
    if game is not None:
        data = get_template_data(game)
    else:
        data = {}
    data["includeGame"] = game is not None
    return fill_template(create_env(), "main_template.jinja2", data)


def player_bar(game, cur_plyr_name):
    tenv = create_env()
    template_data = {"players": [{"name": plyr.name, "color": plyr.color} for plyr in game.players],
                     "cur_plyr_name": cur_plyr_name}
    players_html = fill_template(tenv, "player_bar_template.jinja2", template_data)
    return players_html


def fill_tiles(game):
    tenv = create_env()
    data = get_template_data(game)
    ports = fill_template(tenv, "port_tiles_template.jinja2", data)
    tiles = fill_template(tenv, "tiles_template.jinja2", data)
    numbers = fill_template(tenv, "numbers_template.jinja2", data)
    return ports, tiles, numbers
