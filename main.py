from view.view import Application
import tkinter as tk
from model.game_generator import generate_catan_game


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def start_settle_selection(self):
        avail = self.model.get_available_nodes()
        self.view.display_settle_options(avail)

    def handle_settle_build(self, node):
        self.model.build_settle(node)


def main():
    game = generate_catan_game()
    root = tk.Tk()
    app = Application(game, master=root)
    controller = Controller(game, app)
    app.controller = controller
    app.mainloop()


if __name__ == '__main__':
    main()
