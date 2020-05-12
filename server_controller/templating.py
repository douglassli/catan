from jinja2 import Environment, PackageLoader, select_autoescape
from model.resources import Resource


def get_template_data(tiles_list):
    resource_map = {
        Resource.STONE.name: "#stoneTile",
        Resource.SHEEP.name: "#sheepTile",
        Resource.BRICK.name: "#brickTile",
        Resource.WOOD.name: "#woodTile",
        Resource.WHEAT.name: "#wheatTile",
        Resource.DESERT.name: "#desertTile"
    }

    template_data = {}
    for tile in tiles_list:
        template_data["tile{}_{}".format(tile.row, tile.col)] = resource_map[tile.resource]
        template_data["num{}_{}".format(tile.row, tile.col)] = "#num{}".format(tile.roll_num)

    return template_data


def fill_template(template_name, template_data):
    template_env = Environment(loader=PackageLoader('server_controller', 'templates'),
                               autoescape=select_autoescape(['html', 'xml']))

    template = template_env.get_template(template_name)
    return template.render(template_data)


def create_page(tiles_list):
    return fill_template("svg_template.html", get_template_data(tiles_list))


def create_board(tiles_list):
    return fill_template("svg_board_template.html", get_template_data(tiles_list))


if __name__ == '__main__':
    from model.game_generator import generate_catan_game
    game = generate_catan_game()
    print(create_board(game.tiles.values()))
