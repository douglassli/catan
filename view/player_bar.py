import tkinter as tk
from view.player_frame import PlayerFrame


class PlayerBar(tk.Frame):
    def __init__(self, width, height, master=None):
        super().__init__(master, bg="#0349fc")

        self.p_frames = []
        num_players = 4
        p_height = (height - (num_players * 2) * 5) / num_players

        for i in range(num_players):
            p_frame = PlayerFrame(width, p_height, master=self)
            p_frame.grid(row=i, pady=5)
            self.p_frames.append(p_frame)

    def update_player_info(self, player_states):
        for i, p_frame in enumerate(self.p_frames):
            p_frame.update_info(player_states[i])
