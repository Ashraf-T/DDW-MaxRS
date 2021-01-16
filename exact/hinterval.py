class HInterval:

    def __init__(self, y, inv):
        self.y = y
        self.inv = inv

    @classmethod
    def fromHInterval(cls, hinv):
        return cls(hinv.y, hinv.inv)

    def __lt__(self, other):
        if self.y == other.y:
            return self.inv.weight < other.inv.weight
        else:
            return self.y < other.y

    def __eq__(self, other):
        return self.y == other.y and self.inv.weight == other.inv.weight

    def getY(self):
        return self.y

    def getInv(self):
        return self.inv

    def isAdjacent(self, hInv):
        return self.y == hInv.y and self.inv.isAdjacent(hInv.inv)

    def mergeWith(self, hInv):
        if not self.isAdjacent(hInv):
            raise ValueError('Not mergeable')
        else:
            self.inv.mergeWith(hInv.getInv())

    def __str__(self):
        return f'{self.y} {self.inv}'

