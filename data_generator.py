import random
import math
from point import Point

class DataGenerator():

    def __init__(self, n:int, x_min, y_min, x_max, y_max, a, b, x_ratio, y_ratio,  w_min, w_max, dFactor_min, dFactor_max):

        self.n = n

        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

        self.width = a * y_ratio
        self.length = b * x_ratio

        self.y_n = math.floor(abs(self.y_max - self.y_min) / self.width)
        self.x_n = math.floor(abs(self.x_max - self.x_min) / self.length)

        self.w_min = w_min
        self.w_max = w_max

        self.dFactor_min = dFactor_min
        self.dFactor_max = dFactor_max

        self.points = []

    def generate_points_uniform(self, n=None, t=0):

        if self.dFactor_max == self.dFactor_min: dFactor = self.dFactor_min
        if self.w_max == self.w_min: w_init = self.w_min

        new_points = []
        if not n:
            n = self.n

        for i in range(n):

            x = random.uniform(self.x_min, self.x_max)
            y = random.uniform(self.y_min, self.y_max)

            new_points.append(Point(x, y, t, w_init, dFactor))

        self.points.extend(new_points)
        return new_points

    def generate_points_gaussian(self, n=None, t=0, mu=0.0, sigma=1.0):

        temp_n = 0
        if self.dFactor_max == self.dFactor_min: dFactor = self.dFactor_min
        if self.w_max == self.w_min: w_init = self.w_min

        new_points = []
        if not n:
            n = self.n

        while temp_n < n:

            x = random.gauss(mu, sigma)
            y = random.gauss(mu, sigma)

            if 0 <= x <= self.x_max and 0 <= y <= self.y_max:
                new_points.append(Point(x, y, t, w_init, dFactor))
                temp_n += 1

        self.points.extend(new_points)
        print('generated: {}, wanted: {}'.format(temp_n, n))
        return new_points

    def _generate_points_uniform_cell(self, n=None, t=0):

        if self.dFactor_max == self.dFactor_min: dFactor = self.dFactor_min
        if self.w_max == self.w_min: w_init = self.w_min

        new_points = []
        if not n:
            n = self.n

        for i in range(n):

            x = random.randint(0, self.x_n)
            y = random.randint(0, self.y_n)

            new_points.append(Point(x, y, t, w_init, dFactor))

        return new_points

    def _generate_points_in_cell(self, distribution='uniform'):

        if distribution == 'uniform':

            x = random.uniform(0, self.length)
            y = random.uniform(0, self.width)

        else:
            raise ValueError(" not implemented yet! ")

        return (x, y)

    def generate_points(self, n=None, distribution='uniform', t=0):

        if self.dFactor_max == self.dFactor_min: dFactor = self.dFactor_min
        if self.w_max == self.w_min: w_init = self.w_min

        points = []

        if not n:
            n = self.n

        points_cells = self._generate_points_uniform_cell(n)
        for (i, j) in points_cells:
            (x, y) = self._generate_points_in_cell(distribution)
            points.append(Point(i * self.length + x, j * self.width + y, t, w_init, dFactor))

        return points

    def write_to_file(self, fileName):

        with open(fileName, 'w') as file:
            for p in self.points:
                file.write('{:.2f} {:.2f} {} {} {}'.format(p.x, p.y, p.t_added, p.weight, p.decay_factor))
                file.write('\n')
