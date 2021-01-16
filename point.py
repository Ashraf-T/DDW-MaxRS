from parameters import Experiment_Setup
from exact.hinterval import HInterval
from exact.interval import Interval
import math

class Point:

    def __init__(self, x, y, time, weight, decay):
        self.x = x
        self.y = y
        self.t_added = time
        self.weight = weight
        self.ini_weight = weight
        self.decay_factor = decay

    @classmethod
    def fromPoint(cls, p):
        return cls(p.x, p.y, p.t_added, p.weight, p.decay_factor)

    def __lt__(self, other):
        if self.y == Point(other).y:
            return self.x < Point(other).x
        else:
            return self.y < Point(other).y

    def __eq__(self, other):
        return self.x == Point(other).x and self.y == Point(other).y

    def __str__(self):
        return f'{self.x} {self.y} {self.t_added} {self.weight} {self.decay_factor}'

    def decay_weight(self):
        self.weight = self.weight * self.decay_factor

    def point_update_weight(self, t):
        self.weight = self.ini_weight * (self.decay_factor ** (t - self.t_added))

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getWeight(self):
        return self.weight

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def getXInterval(self):
        return  Interval(self.x - Experiment_Setup.b / 2, self.x + Experiment_Setup.b / 2, 0)

    def getHInterval(self, t):
        y_top = self.y + Experiment_Setup.a / 2
        y_bottom = self.y - Experiment_Setup.a / 2

        inv_top = Interval(round(self.x - Experiment_Setup.b / 2,2) , round(self.x + Experiment_Setup.b / 2, 2), -self.getWeight())
        inv_bottom = Interval(round(self.x - Experiment_Setup.b / 2, 2), round(self.x + Experiment_Setup.b / 2, 2), self.getWeight())

        return [HInterval(y_bottom, inv_bottom), HInterval(y_top, inv_top)]

    def equals(self, p):
        return self.x == p.x and self.y == p.y and self.t_added == p.t_added

    def distance(self, p):
        dx = self.x - p.x
        dy = self.y - p.y
        return math.sqrt(dx * dx + dy * dy)

    def midPoint(self, point):
        return Point((self.x + point.x) / 2, (self.y + point.y) / 2, 0)