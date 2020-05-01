import tkinter as tk


class ButtonBar(tk.Frame):
    def __init__(self, button_mapping, master=None):
        super().__init__(master, bg="#0349fc")
        self.master = master

        self.b_frames = []

        for name, action in button_mapping.items():
            b_frame = tk.Frame(master=self, bg="gray", bd=4, relief=tk.RIDGE)
            label = tk.Label(master=b_frame, text=name)
            label.grid()
            self.b_frames.append(b_frame)
            b_frame.bind("<Button-1>", action)
            label.bind("<Button-1>", action)

        for i, b_frame in enumerate(self.b_frames):
            b_frame.grid(row=0, column=i, padx=5, pady=5)
