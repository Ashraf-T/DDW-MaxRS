from exact.hinterval import HInterval
from exact.interval import Interval
from exact.env import Env
import math

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def fromPoint(cls, p):
        return cls(p.x, p.y)

    def __lt__(self, other):
        if self.y == Point(other).y:
            return self.x < Point(other).x
        else:
            return self.y < Point(other).y

    def __eq__(self, other):
        return self.x == Point(other).x and self.y == Point(other).y

    def __str__(self):
        return f'{self.x} {self.y}'

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def getXInterval(self):
        return  Interval(self.x - Env.width / 2, self.x + Env.width / 2, 0)

    def getHInterval(self):
        y_top = self.y + Env.height / 2
        y_bottom = self.y - Env.height / 2

        inv_top = Interval(self.x - Env.width / 2, self.x + Env.width / 2, -1)
        inv_bottom = Interval(self.x - Env.width / 2, self.x + Env.width / 2, 1)

        return [HInterval(y_bottom, inv_bottom), HInterval(y_top, inv_top)]

    def equals(self, p):
        return self.x == p.x and self.y == self.y

    def distance(self, p):
        dx = self.x - p.x
        dy = self.y - p.y
        return math.sqrt(dx * dx + dy * dy)

    def midPoint(self, point):
        return Point((self.x + point.x) / 2, (self.y + point.y) / 2)