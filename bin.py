import numpy as np
from point import Point
from parameters import Experiment_Setup

class Bin:

    def __init__(self, i, j, last_update=None):

        self.i = i
        self.j = j

        self.last_update = last_update
        self.points = np.empty(0, dtype=Point)
        self.weight = 0


    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

    def getI(self):
        return self.i

    def getJ(self):
        return self.j

    def getWeight(self):
        return self.weight

    def getLastUpdate(self):
        return self.last_update

    def setLastUpdate(self, t):
        self.last_update = t

    def bin_update_weight(self, t):
        w = 0
        for p in self.points:
            p.point_update_weight(t)
            w += p.getWeight()
        self.weight = w

    def add_point(self, p, t):
        self.points = np.append(self.points, p)
        self.bin_update_weight(t)
        self.setLastUpdate(t)

    def extBin_centerd_at_bin(self):
        extBins = []
        temp_extBin_bins = ExtBin(self.i, self.j).bins
        for ii in range(len(temp_extBin_bins)):
            for jj in range(len(temp_extBin_bins[0])):
                b = temp_extBin_bins[ii, jj]
                extBins.append((b.i, b.j))
        return extBins

    def extBins_contain_bin(self):
        extBins = []
        temp_extBin_bins = ExtBin(self.i - (Experiment_Setup.x_ratio - 1), self.j - (Experiment_Setup.y_ratio - 1)).bins
        for ii in range(len(temp_extBin_bins)):
            for jj in range(len(temp_extBin_bins[0])):
                b = temp_extBin_bins[ii, jj]
                extBins.append((b.i, b.j))
        return extBins

    def doubleExtBin_centered_at_bin(self):
        doubleExtBins = []
        temp_doubleExtBin_bins = DoubleExtBin(self.i, self.j).bins
        for ii in range(len(temp_doubleExtBin_bins)):
            for jj in range(len(temp_doubleExtBin_bins[0])):
                b = temp_doubleExtBin_bins[ii, jj]
                doubleExtBins.append((b.i, b.j))
        return doubleExtBins

class ExtBin:

    def __init__(self, i, j, last_update=None):

        self.center = (i, j)
        self.bins = np.empty(shape=(Experiment_Setup.x_ratio, Experiment_Setup.y_ratio), dtype=Bin)
        for x in range(Experiment_Setup.x_ratio):
            for y in range(Experiment_Setup.y_ratio):
                self.bins[x, y] = Bin(i + x, j + y)

        self.weight = 0
        self.last_update = last_update

    def __eq__(self, other):
        return self.center == other.center

    def getWeight(self):
        return self.weight

    def getLastUpdate(self):
        return self.last_update

    def extBin_update_weight(self, t):
        w = 0
        for b in self.bins:
            b.bin_update_weight(t)
            w += b.getWeight()
        self.total_weight = w
        self.setLastUpdate(t)

    def setLastUpdate(self, t):
        self.last_update = t

    def add_point(self, p, t, mapped_bin):
        self.bins[mapped_bin.i - self.center[0], mapped_bin.j - self.center[1]].add_point(p, t)
        self.extBin_update_weight(t)

class DoubleExtBin:

    def __init__(self, i, j, last_update=None):
        self.center = (i, j)
        self.last_update = last_update
        self.weight = 0

        self.bins = np.empty(shape=(3 * Experiment_Setup.x_ratio, 3 * Experiment_Setup.y_ratio), dtype=Bin)
        for x in range(3 * Experiment_Setup.x_ratio):
            for y in range(3 * Experiment_Setup.y_ratio ):
                self.bins[x, y] = Bin(i - Experiment_Setup.x_ratio + x, j - Experiment_Setup.y_ratio + y)

    def __eq__(self, other):
        return self.center == other.center

    def getWeight(self):
        return self.weight

    def getLastUpdate(self):
        return self.last_update

    def doubleExtBin_update_wight(self, t):
        w = 0
        for b in self.bins:
            b.bin_update_weight(t)
            w += b.getWeight()
        self.weight = w
        self.setLastUpdate(t)

    def setLastUpdate(self, t):
        self.last_update = t

    def add_point(self, point, t, mapped_bin):
        self.bins[mapped_bin.i - self.center[0], mapped_bin.j - self.center[1]].add_poit(point, t)
        self.doubleExtBin_update_wight(t)