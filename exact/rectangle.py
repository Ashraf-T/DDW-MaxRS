from exact.point import Point
from exact.interval import Interval

class Rectangle:

    def __init__(self, center_point, width, height, weight=1):

        self.p1 = Point(center_point.getX() - width / 2, center_point.getY() - height / 2, )
        self.p2 = Point(center_point.getX() + width / 2, center_point.getY() + height / 2)
        self.weight = weight

    @classmethod
    def fromPointsWithWeight(cls, p1, p2, weight):
        p = p1.midPoint(p2)
        width = p2.getX() - p1.getX()
        height = p2.getY() - p2.getY()
        return cls(p, width, height, weight)

    def __str__(self):
        return f'{self.p1} {self.p2} {self.weight}'

    def getW(self):
        return int(self.p2.getX()) - int(self.p1.getX())

    def getH(self):
        return int(self.p2.getY() - int(self.p2.getY()))

    def getIntersect(self, r):

        x1 = max(int(self.p1.getX(), int(r.p1.getX())))
        x2 = min(int(self.p2.getX(), int(r.p2.getX())))
        y1 = max(int(self.p1.getY(), int(r.p1.getY())))
        y2 = min(int(self.p2.getY(), int(r.p2.getY())))

        if x1 <= x2 and y1 <= y2:
            return Rectangle.fromPoints(Point(x1, y1), Point(x2, y2))
        else:
            return None

    def getInvX(self):
        return Interval(int(self.p1.getX()), int(self.p2.getX()), self.weight)

    def getInvY(self):
        return Interval(int(self.p1.getY()), int(self.p2.getY()), self.weight)

    def getWeight(self):
        return self.weight

    def setWeight(self, weight):
        self.weight = weight

    def incrementWeight(self, weight=1):
        self.weight += weight

    def getCenter(self):
        return self.p1.midPoint(self.p2)

    def contain(self, point):
        return self.p1.getX() < point.getX() and self.p1.getY() < point.getY() and self.p2.getX() > point.getX() and self.p2.getY() > point.getY()
