from jinja2 import Environment, PackageLoader, select_autoescape
from model.resources import Resource


def create_page(data):
    template_env = Environment(
        loader=PackageLoader('server_controller', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    resource_map = {
        Resource.STONE.name: "#stoneTile",
        Resource.SHEEP.name: "#sheepTile",
        Resource.BRICK.name: "#brickTile",
        Resource.WOOD.name: "#woodTile",
        Resource.WHEAT.name: "#wheatTile",
        Resource.DESERT.name: "#desertTile"
    }

    template_data = {}
    for tile in data["tiles"]:
        template_data["tile{}_{}".format(tile["row"], tile["col"])] = resource_map[tile["resource"]]
        template_data["num{}_{}".format(tile["row"], tile["col"])] = "#num{}".format(tile["rollNum"])

    template = template_env.get_template("svg_template.html")
    return template.render(template_data)


if __name__ == '__main__':
    from model.game_generator import generate_catan_game
    game = generate_catan_game()
    create_page(game.as_data())
