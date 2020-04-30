from view.catan_view import Application
import tkinter as tk
from model.game_generator import generate_catan_game
from controller.catan_control import Controller


def main():
    game = generate_catan_game()
    root = tk.Tk()
    app = Application(game, master=root)
    controller = Controller(game, app)
    app.controller = controller
    controller.start_game()
    app.mainloop()


if __name__ == '__main__':
    main()
