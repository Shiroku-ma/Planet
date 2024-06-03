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
uranus = Asteroid(
    0.773, 74.024, 173.027,
    19.2184, 0.0464, 244.910, 30688.4876,
    "#0fcab3", "uranus"
)
neptune = Asteroid(
    1.770, 131.783, 48.127,
    30.1104, 0.0095, 309.193, 60182.2790,
    "#008cff", "neptune"
)
pluto = Asteroid(
    17.1, 110.3, 225.0,
    39.592, 0.248, 47.9, 90582.00,
    "#bcbcbc", "pluto"
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
        
        self.date = self.to_jd(2024,6,1)
        self.zoom = 0
        self.angle_x = 0
        self.angle_z = 0
        self.cache_orbit()
        self.create_win2()
        self.draw_orbit()
        self.plot_all()

        root.bind("<KeyPress>", self.key_event)

    def key_event(self, e):
        key = e.keysym
        if key in ["Up", "Down", "Right", "Left"]:
            if key == "Up":
                self.zoom += 1
                self.label_zoom["text"] = f"倍率: {self.zoom:3}"
                self.draw_orbit()
            if key == "Down":
                self.zoom -= 1
                self.label_zoom["text"] = f"倍率: {self.zoom:3}"
                self.draw_orbit()
            if key == "Right":
                self.date += 1
            if key == "Left":
                self.date -= 1
            self.plot_all()
        if key in ["s", "w", "a", "d"]:
            if key == "s":
                if self.angle_x < 90:
                    self.angle_x += 5
            if key == "w":
                if self.angle_x > 0:
                    self.angle_x -= 5
            if key == "a":
                self.angle_z += 5
                if self.angle_z > 180:
                    self.angle_z = -175
            if key == "d":
                self.angle_z -= 5
                if self.angle_z <= -180:
                    self.angle_z = 180
            self.label_angle_x["text"] = f"x軸: {self.angle_x:4}"
            self.label_angle_z["text"] = f"z軸: {self.angle_z:4}"
            self.draw_orbit()
            self.plot_all()

    def cache_orbit(self):
        self.cached_orbit = {}
        for ast in [mercury,venus,earth,mars,jupiter,saturn,uranus,neptune,pluto]:
            self.cached_orbit[ast.name] = []
            i = 0
            h = ast.P / 180
            for j in range(180):
                self.cached_orbit[ast.name].append(ast.get_position(i))
                i += h
            
    def draw_orbit(self):
        self.canvas.delete("orbit")
        for ast in [mercury,venus,earth,mars,jupiter,saturn,uranus,neptune,pluto]:
            for j in range(180):
                self.plot(self.cached_orbit[ast.name][j], "#fff", "orbit", 0.5)

    def plot_all(self):
        for ast in [mercury,venus,earth,mars,jupiter,saturn,uranus,neptune,pluto]:
            self.canvas.delete(ast.name)
            self.plot(ast.get_position(self.date), ast.color, ast.name, 4)

    def plot(self, position :np.ndarray, color : str, name, weight):
        x = radians(self.angle_x)
        z = radians(self.angle_z)
        xr = np.array([
            [1.0,0,0],
            [0,cos(x),-sin(x)],
            [0,sin(x),cos(x)]
        ])
        zr = np.array([
            [cos(z),-sin(z),0],
            [sin(z),cos(z),0],
            [0,0,1.0]
        ])
        pos = xr @ zr @ position
        _zoom = 200 * 1.05 ** self.zoom
        x = pos[0][0] * _zoom
        y = pos[1][0] * _zoom
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

    def to_jd(self, year, month, day):
        mjd = floor(year * 365.25) + floor(year/400) - floor(year/100) + floor(30.59 * (month - 2)) + day - 678912.0 + 2400000.5
        return mjd
    
    def to_date(self, jd):
        n = jd - 2400000.5 + 678881
        a = 4*n + 3 + 4 * floor(3 / 4 * floor(4*(n+1)/146097 + 1))
        b = 5 * floor((a % 1461) / 4) +2
        y = floor(a/1461)
        m = floor(b/153) + 3
        d = floor((b%153)/5) + 1
        return [y,m,d]
    
    def date_changed(self):
        jd = self.to_jd(float(self.spinbox_y.get()), float(self.spinbox_m.get()), float(self.spinbox_d.get()))
        self.date = jd
        self.plot_all()

    
    def create_win2(self):
        self.controller = tk.Toplevel(self)
        self.controller.geometry("210x300")
        self.controller.title(u"Controller")
        self.spinbox_y = tk.Spinbox(
            self.controller,
            from_=1583, to=3000, increment=1,
            command=self.date_changed,
            width=5,
            textvariable=tk.IntVar(value=2024)
            )
        self.spinbox_m = tk.Spinbox(
            self.controller,
            from_=1, to=12, increment=1,
            command=self.date_changed,
            width=2,
            textvariable=tk.IntVar(value=1)
            )
        self.spinbox_d = tk.Spinbox(
            self.controller,
            from_=1, to=31, increment=1,
            command=self.date_changed,
            width=2,
            textvariable=tk.IntVar(value=1)
            )
        h_date = tk.Label(
            self.controller,
            text="日付",
            font=("Helvetica",16)
            )
        label_y = tk.Label(
            self.controller,
            text="年",
            )
        label_m = tk.Label(
            self.controller,
            text="月",
            )
        label_d = tk.Label(
            self.controller,
            text="日",
            )
        h_angle = tk.Label(
            self.controller,
            text="視点",
            font=("Helvetica",16)
            )
        self.label_angle_x = tk.Label(
            self.controller,
            text="x軸:     0",
            font=("Helvetica",14)
            )
        self.label_angle_z = tk.Label(
            self.controller,
            text="z軸:     0",
            font=("Helvetica",14)
            )
        self.label_zoom = tk.Label(
            self.controller,
            text="倍率: 200",
            font=("Helvetica",14)
            )
                
        h_date.grid(column=0,row=0)
        self.spinbox_y.grid(column=0,row=1)
        label_y.grid(column=1,row=1)
        self.spinbox_m.grid(column=2,row=1)
        label_m.grid(column=3,row=1)
        self.spinbox_d.grid(column=4,row=1)
        label_d.grid(column=5,row=1)

        h_angle.grid(column=0,row=2)
        self.label_angle_x.grid(column=0,row=3,sticky=tk.W)
        self.label_angle_z.grid(column=0,row=4,sticky=tk.W)
        self.label_zoom.grid(column=0,row=5,sticky=tk.W)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()