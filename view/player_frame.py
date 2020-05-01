import tkinter as tk


class PlayerFrame(tk.Frame):
    def __init__(self, width, height, master=None):
        super().__init__(master, bg="#0349fc")

        self.p_frames = []
        num_players = 4
        p_height = (height - (num_players * 2) * 5) / num_players
        for i in range(num_players):
            p_frame = tk.Frame(master=self, bg="gray", height=p_height, width=width, bd=4, relief=tk.RIDGE)
            self.p_frames.append(p_frame)
            p_frame.grid(row=i, pady=5)

        for i, p_frame in enumerate(self.p_frames):
            p_frame.grid(row=i, pady=5)
