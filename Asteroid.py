from decimal import Decimal


class Asteroid():
    def __init__(self, i : Decimal, Ω : Decimal, ω : Decimal, a : Decimal, e : Decimal, M0 : Decimal):
        """
        Paramaters
        ----------
        i : Decimal
            軌道傾斜角
        Ω : Decimal
            昇交点黄経
        ω : Decimal
            近日点引数
        a : Decimal
            軌道長半径
        e : Decimal
            離心率
        M0 : Decimal
            ユリウス日2455400.5における平均近点角

        """


if __name__ == "__main__":
    mars = Asteroid(1.849, 49.527, 336.107, 1.5237, 0.0934, 239.735)
    