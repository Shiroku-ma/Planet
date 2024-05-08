import numpy as np
from math import *
import tkinter as tk


#軌道傾斜（地球基準）
i = 0
#昇交点黄経
ω = 174.848
#近日点引数
Ω = 102.972
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
        self.plot(self.calc_position(2460390.00486))
        #self.plot(self.calc_position(2460438.50000))

    def plot(self, position :np.ndarray):
        print(position)
        x = position[0][0] * 100
        y = position[1][0] * 100
        self.canvas.create_oval(
            self.__to_canvas_x(x),self.__to_canvas_y(y),
            self.__to_canvas_x(x+1),self.__to_canvas_y(y+1),
            fill="#fff",
            width=0
        )

    def calc_position(self, t):
        E = self.__calc_E(self.__calc_M(t))

        X = a * sin(E)
        Y = sqrt(1 - e ** 2) * a * cos(E)

        a1 = np.array([
            [cos(Ω), -sin(Ω), 0],
            [sin(Ω), cos(Ω), 0],
            [0, 0, 1]
        ])
        a2 = np.array([
            [1, 0],
            [0, cos(i)],
            [0, sin(i)]
        ])
        a3 = np.array([
            [cos(ω), -sin(ω)],
            [sin(ω), cos(ω)]
        ])
        a4 = np.array([
            [X - a * e],
            [Y]
        ])

        return a1 @ a2 @ a3 @ a4

    def __calc_E(self, M):
        E = M
        for j in range(10):
            E = E - (M - E + e * sin(E)) / (e * cos(E) - 1)
        return E

    def __calc_M(self, T):
        M = M0 + 2 * pi * (T - T0) / 365.24219
        return M

    def __to_canvas_x(self, x):
        return CANVAS_WIDTH / 2 + x

    def __to_canvas_y(self, y):
        return CANVAS_HEIGHT / 2 - y

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()