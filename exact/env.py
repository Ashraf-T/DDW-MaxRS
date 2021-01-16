class Env:
    def __init__(self, num_points, a, b):

        self.height = a
        self.width = b

        self.Sample_Num = num_points

        self.ReadCount = 0
        self.WriteCount = 0

        self.Max_Coord = 10
        self.Min_Coord = 0

        self.max = max(self.Max_Coord + self.width, self.Max_Coord + self.height)
        self.min = min(self.Min_Coord - self.width, self.Min_Coord - self.height)
