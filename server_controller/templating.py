from jinja2 import Environment, PackageLoader, select_autoescape
from model.resources import Resource


def get_template_data(tiles_list):
    resource_map = {
        Resource.STONE: "#stoneTile",
        Resource.SHEEP: "#sheepTile",
        Resource.BRICK: "#brickTile",
        Resource.WOOD: "#woodTile",
        Resource.WHEAT: "#wheatTile",
        Resource.DESERT: "#desertTile"
    }

    template_data = {}
    for tile in tiles_list:
        template_data["tile{}_{}".format(tile.row, tile.col)] = resource_map[tile.resource]
        template_data["num{}_{}".format(tile.row, tile.col)] = "#num{}".format(tile.roll_num)

    return template_data


def create_env():
    return Environment(loader=PackageLoader('server_controller', 'templates'),
                       autoescape=select_autoescape(['html', 'xml']))


def fill_template(template_env, template_name, template_data):
    template = template_env.get_template(template_name)
    return template.render(template_data)


def create_page(tiles_list=None):
    if tiles_list is not None:
        data = get_template_data(tiles_list)
    else:
        data = {}
    data["includeGame"] = tiles_list is not None
    return fill_template(create_env(), "main_template.jinja2", data)


def fill_tiles(tiles_list):
    tenv = create_env()
    data = get_template_data(tiles_list)
    ports = fill_template(tenv, "port_tiles_template.jinja2", data)
    tiles = fill_template(tenv, "tiles_template.jinja2", data)
    numbers = fill_template(tenv, "numbers_template.jinja2", data)
    return ports, tiles, numbers
