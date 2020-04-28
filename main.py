from view.catan_view import Application
import tkinter as tk
from model.game_generator import generate_catan_game


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.is_setup = True
        self.is_reverse = False

    def start_settle_selection(self):
        avail = self.model.get_available_settle_nodes(self.is_setup)
        self.view.display_settle_options(avail)

    def handle_settle_build(self, coord):
        color = self.model.build_settle(coord)
        return color

    def start_road_selection(self):
        avail = self.model.get_available_paths()
        self.view.display_road_options(avail)

    def handle_road_build(self, coord):
        color = self.model.build_road(coord)
        if self.is_setup:
            self.handle_turn_change()
        return color

    def handle_turn_change(self):
        self.is_setup, self.is_reverse = self.model.change_turn(self.is_setup, self.is_reverse)

    # def handle_end_setup(self):
    #     self.model.end_setup()


def main():
    game = generate_catan_game()
    root = tk.Tk()
    app = Application(game, master=root)
    controller = Controller(game, app)
    app.controller = controller
    app.mainloop()


if __name__ == '__main__':
    main()
