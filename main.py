import numpy as np
from math import *
import tkinter as tk
from Asteroid import Asteroid

CANVAS_WIDTH = 860
CANVAS_HEIGHT = 860

now = 2460462.50000

mercury = Asteroid(
    7.004, 48.300, 77.495,
    0.3871, 0.2056, 54.463, 87.9705,
    "#555588", "mercury"
)
venus = Asteroid(
    3.394, 76.613, 131.565,
    0.7233, 0.0068, 198.081, 224.7018,
    "#888800", "venus"
)
earth = Asteroid(
    0.003, 174.815, 103.016,
    1.000, 0.0167, 85.512, 365.2574,
    "#5555ff", "earth"
)
mars = Asteroid(
    1.848, 49.487, 336.168,
    1.5237, 0.0934, 339.838, 686.9805,
    "#ff0000", "mars"
)
jupiter = Asteroid(
    1.303, 100.507, 14.384,
    5.2026, 0.0485, 35.782, 4332.5955,
    "#a9569c", "jupiter"
)
saturn = Asteroid(
    2.489, 113.603, 93.195,
    9.5549, 0.0555, 253.185, 10759.2423,
    "#a98c56", "saturn"
)

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
        
        self.date = now
        self.zoom = 200
        self.draw_orbit()
        self.plot_all()

        root.bind("<KeyPress>", self.key_event)

    def key_event(self, e):
        key = e.keysym
        if key == "Up":
            self.zoom += 10
            self.draw_orbit()
        if key == "Down":
            self.zoom -= 10
            self.draw_orbit()
        if key == "Right":
            self.date += 1
        if key == "Left":
            self.date -= 1
        if key == "Up" or key == "Down" or key == "Right" or key == "Left":
            self.plot_all()
            
    def draw_orbit(self):
        self.canvas.delete("orbit")
        for ast in [mercury,venus,earth,mars,jupiter,saturn]:
            i = 0
            while(i < floor(ast.P) + 1):
                self.plot(ast.get_position(i), "#fff", "orbit", 0.5)
                i += floor(ast.P) / 180

    def plot_all(self):
        for ast in [mercury,venus,earth,mars,jupiter,saturn]:
            self.canvas.delete(ast.name)
            self.plot(ast.get_position(self.date), ast.color, ast.name, 4)

    def plot(self, position :np.ndarray, color : str, name, weight):
        x = position[0][0] * self.zoom
        y = position[1][0] * self.zoom
        self.canvas.create_oval(
            self.__to_canvas_x(x-weight),self.__to_canvas_y(y-weight),
            self.__to_canvas_x(x+weight),self.__to_canvas_y(y+weight),
            fill=color,
            width=0,
            tags=name
        )

    def __to_canvas_x(self, x):
        return CANVAS_WIDTH / 2 + x

    def __to_canvas_y(self, y):
        return CANVAS_HEIGHT / 2 - y    

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()