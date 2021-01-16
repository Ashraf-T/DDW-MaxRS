import numpy as np

class Interval:

    def __init__(self, s, e, weight):
        self.s = s
        self.e = e
        self.weight = weight

    def __lt__(self, other):
        return self.s < other.s

    def __eq__(self, other):
        return self.s == other.s and self.e == other.e

    def __str__(self):
        return f'{self.s} {self.e} {self.weight}'

    def getWeightIntersect(self, inv):

        s = max(self.s, inv.s)
        e = min(self.e, inv.e)
        weight = self.weight + inv.weight

        if s < e:
            return Interval(s, e, weight)
        else:
            return None

    def getIntersect(self, inv):

        s = max(self.s, inv.s)
        e = min(self.e, inv.e)
        weight = self.weight + inv.weight

        if s < e:
            return Interval(s, e, weight)
        else:
            return None

    def getDiff(self, inv):

        inetersect = self.getWeightIntersect(inv)
        if not inetersect:
            return np.array([self])

        else:
            diff = []
            if self.s < inetersect.s:
                diff.append(Interval(self.s, inetersect.s, self.weight))
            if inetersect.e < self.e:
                diff.append(Interval(inetersect.e, self.e, self.weight))
            return np.array(diff)

    def mergeWith(self, inv):
        if self.s == inv.e:
            self.s = inv.s
        elif self.e == inv.s:
            self.e = inv.e

    def equalsWithWeight(self, inv):
        return self.equals(inv) and self.weight == inv.weight

    def isAdjacent(self, inv):
        return self.s == inv.e or self.e == inv.s

    def isMergeable(self, inv):
        return self.isAdjacent(inv) and self.weight == inv.weight

    def isCovered(self, inv):
        return self.s >= inv.s and self.e <= inv.e

    def isIntersect(self, inv):
        s = max(self.s, inv.s)
        e = min(self.e, inv.e)
        return s < e

    def isDisjoint(self, inv):
        return not self.isIntersect(inv)

    def isCovers(self, k):
        return self.s <= k <= self.e
