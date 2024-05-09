import numpy as np
from math import sin, cos, pi, sqrt, radians


class Asteroid():
    def __init__(self, i , Ω , ω , a , e , M0 , P ):
        """
        Paramaters
        ----------
        i : float
            軌道傾斜角
        Ω : float
            昇交点黄経
        ω : float
            近日点引数
        a : float
            軌道長半径
        e : float
            離心率
        M0 : float
            ユリウス日2455400.5における平均近点角
        P : float
            公転周期
        """
        self.i = radians(i)
        self.Ω = radians(Ω)
        self.ω = radians(ω)
        self.a = a
        self.e = e
        self.M0 = radians(M0)
        self.P = P
    
    def get_position(self, t):
        E = self.__calc_E(self.__calc_M(t))
        
        X = self.a * sin(E)
        Y = sqrt(1.0 - self.e ** 2) * self.a * cos(E)

        a1 = np.array([
            [cos(self.Ω), -sin(self.Ω), 0],
            [sin(self.Ω), cos(self.Ω), 0],
            [0, 0, 1.0]
        ])
        a2 = np.array([
            [1.0, 0],
            [0, cos(self.i)],
            [0, sin(self.i)]
        ])
        a3 = np.array([
            [cos(self.ω), -sin(self.ω)],
            [sin(self.ω), cos(self.ω)]
        ])
        a4 = np.array([
            [X - self.a * self.e],
            [Y]
        ])
        
        return a1 @ a2 @ a3 @ a4

    def __calc_E(self, M):
        E = M
        for j in range(10):
            E = E - (M - E + self.e * sin(E)) / (self.e * cos(E) - 1.0)
        return E

    def __calc_M(self, t):
        M = self.M0 + 2 * pi * (t - 2455400.5) / self.P
        return M


if __name__ == "__main__":
    print("Hello")
    
