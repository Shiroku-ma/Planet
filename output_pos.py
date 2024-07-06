import numpy as np
import json
from math import *
from Planet import Planet

class Test():
    def __init__(self):
        self.load_jsondata("2005-08-18")
        year = int(input("year: "))
        month = int(input("month: "))
        day = int(input("day: "))
        self.test_positions(year,month,day)

    def load_jsondata(self, date):
        """
        date : YYYY-MM-DD
        """
        colors = {
            "mercury": "#555588", "venus": "#888800", "earth": "#5555ff", "mars": "#ff0000",
            "jupiter": "#a9569c", "saturn": "#a98c56", "uranus": "#0fcab3", "neptune": "#008cff"
        }
        file = open("./data.json", "r")
        data = json.load(file)[date]
        self.planets = [
            Planet(
                data[name]["incl"], data[name]["lan"], data[name]["lperi"], data[name]["a"], data[name]["e"], data[name]["m0"], data[name]["p"], data["epoch"],
                colors[name], name
            ) for name in data.keys() if name !=  "epoch"
        ] #内包表記でゴリ押し

    def test_positions(self, year, month, day):
        jd = self.to_jd(year, month, day)
        for ast in self.planets:
            pos = ast.get_position(jd)
            print(ast.name)
            print("x   " + str(pos[0][0]))
            print("y   " + str(pos[1][0]))
            print("z   " + str(pos[2][0]))
            print()

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


if __name__ == "__main__":
    test = Test()