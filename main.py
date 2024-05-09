import numpy as np
from math import *
import tkinter as tk
from Asteroid import Asteroid


#軌道傾斜（地球基準）
i = 0
#昇交点黄経
Ω = 174.848
#近日点引数
ω = 102.972
#軌道長半径 (AU)
a = 1.0000
#離心率
e = 0.0167 
#2455400.5 ユリウス日の値;2010/7/23 における平均近点角
M0 = 197.510
T0 = 2455400.5

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
        venus = Asteroid(
            3.395, 76.651, 131.564,
            0.7233, 0.0068, 107.429, 224.701
        )
        earth = Asteroid(
            0.0, 174.848, 102.972,
            1.000, 0.0167, 197.510, 365.24219
        )
        mars = Asteroid(
            1.849, 49.527, 336.107,
            1.5237, 0.0934, 239.735, 686.980
        )

        for i in range(1):
            self.plot(venus.get_position(2460438.50000+i), "#888800")
            self.plot(earth.get_position(2460438.50000+i), "#5555ff")
            self.plot(mars.get_position(2460438.50000+i), "#ff0000")

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
        return CANVAS_WIDTH / 2 + int(x)

    def __to_canvas_y(self, y):
        return CANVAS_HEIGHT / 2 - int(y)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()