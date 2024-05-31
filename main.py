import numpy as np
from math import *
import tkinter as tk
from Asteroid import Asteroid

CANVAS_WIDTH = 640
CANVAS_HEIGHT = 640

class App(tk.Frame):
    def __init__(self, root: tk.Tk):
        super().__init__(root)
        root.geometry(f"{CANVAS_WIDTH}x{CANVAS_HEIGHT}")
        self.canvas = tk.Canvas(
            root,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            background="#000",
            borderwidth=0,
            highlightthickness=0
            )
        self.canvas.place(x=0,y=0)
        self.canvas.create_oval(
            self.__to_canvas_x(-5),self.__to_canvas_y(-5),
            self.__to_canvas_x(5),self.__to_canvas_y(5),
            tags="sun",
            fill="#ffff00",
            width=0
            )
        self.mercury = Asteroid(
            7.004, 48.300, 77.495,
            0.3871, 0.2056, 54.463, 87.9705
        )
        self.venus = Asteroid(
            3.394, 76.613, 131.565,
            0.7233, 0.0068, 198.081, 224.7018
        )
        self.earth = Asteroid(
            0.003, 174.815, 103.016,
            1.000, 0.0167, 85.512, 365.2574
        )
        self.mars = Asteroid(
            1.848, 49.487, 336.168,
            1.5237, 0.0934, 339.838, 686.9805
        )
        
        now = 2460389.50000

        for i in range(1):
            self.plot(self.mercury.get_position(now+i), "#555588")
            self.plot(self.venus.get_position(now+i), "#888800")
            self.plot(self.earth.get_position(now+i), "#5555ff")
            self.plot(self.mars.get_position(now+i), "#ff0000")

        #root.after(100, self.move, now)

    def move(self, date):
        self.plot(self.mercury.get_position(date), "#555588")
        self.plot(self.venus.get_position(date), "#888800")
        self.plot(self.earth.get_position(date), "#5555ff")
        self.plot(self.mars.get_position(date), "#ff0000")
        self.after(100, self.move, date+1.0)

    def plot(self, position :np.ndarray, color : str):
        x = position[0][0] * 200
        y = position[1][0] * 200
        self.canvas.create_oval(
            self.__to_canvas_x(x-2),self.__to_canvas_y(y-2),
            self.__to_canvas_x(x+2),self.__to_canvas_y(y+2),
            fill=color,
            width=0
        )

    def __to_canvas_x(self, x):
        return CANVAS_WIDTH / 2 + x

    def __to_canvas_y(self, y):
        return CANVAS_HEIGHT / 2 - y

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()