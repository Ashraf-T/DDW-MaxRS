class HLine:

    def __init__(self, y, inv):
        self.y = y
        self.maxInv = inv

    def getY(self):
        return self.y

    def getMaxInv(self):
        return self.maxInv

    def size(self):
        return HLine.size

    def __str__(self):
        return f'{self.y} {self.maxInv}'
