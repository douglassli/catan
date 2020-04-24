from model.catan_game import CatanGame
from view.view import Application
import tkinter as tk


def main():
    game = CatanGame()
    root = tk.Tk()
    app = Application(game, master=root)
    app.mainloop()


if __name__ == '__main__':
    main()
