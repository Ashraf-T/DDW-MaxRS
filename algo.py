from exact.record_file import HInvFile, HLineFile, PointFile
from exact.exact_algorithm_ram import AlgorithmRAM
from parameters import Experiment_Setup, ExactEnv
from exact.interval import Interval
from bin import Bin, DoubleExtBin
from point import Point
import numpy as np
import logging
import math
import os

class Grid:

    def __init__(self):

        self.bin_height = Experiment_Setup.a / Experiment_Setup.y_ratio
        self.bin_width = Experiment_Setup.b / Experiment_Setup.x_ratio

        self.y_n = math.ceil(abs(Experiment_Setup.y_max - Experiment_Setup.y_min) / self.bin_height) + 1
        self.x_n = math.ceil(abs(Experiment_Setup.x_max - Experiment_Setup.x_min) / self.bin_width) + 1

        self.bins_dict = {}
        self.extBins_dict = {}

        self.grid = np.zeros((self.x_n, self.y_n))

    def getNonEmptyBins(self):
        return self.n_NonEmtpy

    def getWidth(self):
        return self.bin_height

    def getLength(self):
        return self.bin_width

    def _is_valid_bin(self, center):
        i, j = center[0], center[1]
        return 0 <= i <= self.x_n and 0 <= j <= self.y_n

    def map_point_to_bin(self, point):
        mapped_bin = (math.floor(abs(point.x - Experiment_Setup.x_min) / self.bin_width), math.floor(abs(point.y - Experiment_Setup.y_min) / self.bin_height))
        if mapped_bin not in self.bins_dict.keys() and self._is_valid_bin(mapped_bin): self.bins_dict[mapped_bin] = Bin(mapped_bin[0], mapped_bin[1])
        return mapped_bin

    def map_point_to_extBins(self, point):
        mapped_bin = self.map_point_to_bin(point)
        mapped_extBins = Bin(mapped_bin[0], mapped_bin[1]).extBins_contain_bin()
        for b in mapped_extBins:
            if b not in self.extBins_dict.keys() and self._is_valid_bin(b):
                self.extBins_dict[b] = Bin(b[0], b[1]).extBin_centerd_at_bin()
        return mapped_extBins

    def add_point_to_bin(self, point, t):
        mapped_bin = self.map_point_to_bin(point)
        if self._is_valid_bin(mapped_bin):
            self.bins_dict[self.map_point_to_bin(point)].add_point(point, t)

    def add_point(self, point, t):
        self.add_point_to_bin(point, t)
        self.map_point_to_extBins(point)
        self.grid[self.map_point_to_bin(point)[0], self.map_point_to_bin(point)[1]] += 1

    def load_of_bin(self, bin):
        return self.grid[bin.i, bin.j]

    def weight_of_bin(self, bin):
        if (bin.i, bin.j) not in self.bins_dict.keys():
            return self.bins_dict[(bin.i, bin.j)].getWeight()
        else: return 0

    def weight_of_extBin(self, extBin):
        if extBin not in self.extBins_dict.keys(): return 0
        else:
            w = 0
            for b in self.extBins_dict[extBin]:
                if b in self.bins_dict.keys():
                    w += self.bins_dict[b].getWeight()
            return w

    def max_load_bins(self):
        return np.amax(self.grid)

    def update_all_bins_weights(self, t):
        for b in self.bins_dict.values():
            b.bin_update_weight(t)

    def update_bin_weight(self, bin, t):
        if bin in self.bins_dict.keys(): self.bins_dict[bin].bin_update_weight(t)

    def update_extBin_weight(self, extBin, t):
        if extBin in self.extBins_dict.keys():
            for b in self.extBins_dict[extBin]:
                if b in self.bins_dict.keys():
                    self.bins_dict[b].bin_update_weight(t)

    def update_weight(self, t):
        self.update_all_bins_weights(t)

    def max_bin_weight(self, t):
        self.update_all_bins_weights(t)
        max_bin = max(self.bins_dict.keys(), key=lambda k: self.weight_of_bin(k))
        return max_bin, self.bins_dict[max_bin].getWeight()

    def max_extBin_weight(self, t):
        self.update_all_bins_weights(t)
        max_extBin = max(self.extBins_dict.keys(), key=lambda k: self.weight_of_extBin(k))
        return max_extBin, self.weight_of_extBin(max_extBin)


class exactMaxRS_Naive:

    def __init__(self, path):
        self.points = np.empty(0, dtype=Point)
        self.maxRS = None
        self.maxRS_lastUpdate = None
        self.dsFname = os.path.join(path, 'points_exact_naive')

    def setLastUpdate(self, t):
        self.maxRS_lastUpdate = t

    def add_point(self, point, t):
        self.points = np.append(self.points, point)

    def write_points_to_file(self, t, points, x_min, x_max, y_min, y_max):

        if os.path.exists(self.dsFname): os.remove(self.dsFname)

        if points is None:
            points = self.points

        n_points = 0
        with open(self.dsFname, 'w') as file:
            for p in self.points:
                file.write('{:.2f} {:.2f} {} {} {}'.format(p.x, p.y, p.t_added, p.weight, p.decay_factor))
                file.write('\n')
                n_points += 1

        self.update_env_parameters(n_points, x_min, x_max, y_min, y_max)

    def update_env_parameters(self, n_points, x_min, x_max, y_min, y_max):
        ExactEnv.Min_Coord = min(x_min, y_min)
        ExactEnv.Max_Coord = max(x_max, y_max)

        ExactEnv.max = max(ExactEnv.Max_Coord + Experiment_Setup.b, ExactEnv.Max_Coord + Experiment_Setup.a)
        ExactEnv.min = min(ExactEnv.Min_Coord - Experiment_Setup.b, ExactEnv.Min_Coord - Experiment_Setup.a)

        ExactEnv.Sample_Num = n_points

    def exact_maxRS(self, t, points=None, x_min=Experiment_Setup.x_min, x_max=Experiment_Setup.x_max, y_min=Experiment_Setup.y_min, y_max=Experiment_Setup.y_max):
        self.write_points_to_file(t, points, x_min, x_max, y_min, y_max)

        rectFname = self.preprocess(self.dsFname, t)
        finDstname = 'final_naive'
        with open(finDstname, 'w') as file: pass

        scrFile = HInvFile(rectFname)
        scrList = []
        for i in range(scrFile.recordsNum):
            scrList.append(scrFile.get(i))

        algRam = AlgorithmRAM(scrList, Interval(ExactEnv.min, ExactEnv.max, 0))
        maxRect = algRam.exactMaxRS()

        dstFile = HLineFile(finDstname)
        for hLine in algRam.getOutputSet():
            dstFile.insert(hLine)
        dstFile.close()
        file.close()

        return maxRect

    def complete_exact_maxRS(self, t):
        self.update_all_points_weights(t)
        self.maxRS = self.exact_maxRS(t)
        self.setLastUpdate(t)

    def update_all_points_weights(self, t):
        for p in self.points:
            p.point_update_weight(t)

    def preprocess(self, fname, t):

        pointFile_name = fname
        hInvFile_name = fname + 'hInv'
        if os.path.exists(hInvFile_name): os.remove(hInvFile_name)

        point_file = PointFile(pointFile_name)
        hInv_file = HInvFile(hInvFile_name)

        if not hInv_file.empty(): hInv_file.clear()

        for i in range(ExactEnv.Sample_Num):

            p = Point.fromPoint(point_file.get(i))
            hInv_file.insert(p.getHInterval(t)[0])
            hInv_file.insert(p.getHInterval(t)[1])

        point_file.close()

        hInv_file.ramSort()
        hInv_file.close()

        return hInvFile_name

    def update_maxRS_NoEntry(self, t):
        self.update_all_points_weights(t) # not necessary - can be removed
        self.maxRS = self.maxRS * (Experiment_Setup.decay_factor ** (t - self.maxRS_lastUpdate))
        self.setLastUpdate(t)

    def update_exact_solution(self, p, t):

        self.update_maxRS_NoEntry(t)

        sub_space = [p.x - Experiment_Setup.b, p.x + Experiment_Setup.b, p.y - Experiment_Setup.a, p.y + Experiment_Setup.a]
        temp_points = np.empty(0, dtype=Point)
        for p in self.points:
            if sub_space[0] <= p.x <= sub_space[1] and sub_space[2] <= p.y <= sub_space[3]:
                np.append(temp_points, p)

        temp_maxRS = self.exact_maxRS(t, temp_points, sub_space[0], sub_space[1], sub_space[2], sub_space[3])
        if temp_maxRS > self.maxRS:
            self.maxRS = temp_maxRS
            self.setLastUpdate(t)

        return self.maxRS


class exactMaxRS(Grid):

    def __init__(self, path):
        super().__init__()

        self.maxRS = None
        self.maxRS_lastUpdate = None

        self.dsFname = os.path.join(path, 'points_exact')

    def setLastUpdate(self, t):
        self.maxRS_lastUpdate = t

    def write_points_to_file(self, t, bins, x_min, x_max, y_min, y_max):

        if os.path.exists(self.dsFname): os.remove(self.dsFname)

        if bins == None:
            bins = self.bins_dict.values()

        n_points = 0
        with open(self.dsFname, 'w') as file:
            for b in bins:
                for p in b.points:
                    file.write('{:.2f} {:.2f} {} {} {}'.format(p.x, p.y, p.t_added, p.weight, p.decay_factor))
                    file.write('\n')
                    n_points += 1

        self.update_env_parameters(n_points, x_min, x_max, y_min, y_max)

    def update_env_parameters(self, n_points, x_min, x_max, y_min, y_max):
        ExactEnv.Min_Coord = min(x_min, y_min)
        ExactEnv.Max_Coord = max(x_max, y_max)

        ExactEnv.max = max(ExactEnv.Max_Coord + Experiment_Setup.b, ExactEnv.Max_Coord + Experiment_Setup.a)
        ExactEnv.min = min(ExactEnv.Min_Coord - Experiment_Setup.b, ExactEnv.Min_Coord - Experiment_Setup.a)

        ExactEnv.Sample_Num = n_points

    def exact_maxRS(self, t, bins=None, x_min=Experiment_Setup.x_min, x_max=Experiment_Setup.x_max, y_min=Experiment_Setup.y_min, y_max=Experiment_Setup.y_max):

        self.write_points_to_file(t, bins, x_min, x_max, y_min, y_max)
        rectFname = self.preprocess(self.dsFname, t)
        finDstname = 'final'
        with open(finDstname, 'w') as file: pass

        scrFile = HInvFile(rectFname)
        scrList = []
        for i in range(scrFile.recordsNum):
            scrList.append(scrFile.get(i))

        algRam = AlgorithmRAM(scrList, Interval(ExactEnv.min, ExactEnv.max, 0))
        maxRect = algRam.exactMaxRS()

        dstFile = HLineFile(finDstname)
        for hLine in algRam.getOutputSet():
            dstFile.insert(hLine)
        dstFile.close()
        file.close()

        return maxRect

    def complete_exact_maxRS(self, t):
        self.update_all_bins_weights(t)
        self.maxRS = self.exact_maxRS(t)
        self.setLastUpdate(t)

    def preprocess(self, fname, t):

        pointFile_name = fname
        hInvFile_name = fname + 'hInv'
        if os.path.exists(hInvFile_name): os.remove(hInvFile_name)

        point_file = PointFile(pointFile_name)
        hInv_file = HInvFile(hInvFile_name)

        if not hInv_file.empty(): hInv_file.clear()

        for i in range(ExactEnv.Sample_Num):

            p = Point.fromPoint(point_file.get(i))
            # p.point_update_weight(t)
            hInv_file.insert(p.getHInterval(t)[0])
            hInv_file.insert(p.getHInterval(t)[1])

        point_file.close()

        hInv_file.ramSort()
        hInv_file.close()

        return hInvFile_name

    def update_maxRS_NoEntry(self, t):
        self.update_all_bins_weights(t) # not necessary - can be removed
        self.maxRS = self.maxRS * (Experiment_Setup.decay_factor ** (t - self.maxRS_lastUpdate))
        self.setLastUpdate(t)

    def update_exact_solution(self, p, t):

        self.update_maxRS_NoEntry(t)
        mapped_bin = self.map_point_to_bin(p)
        mapped_doubleExtBin = DoubleExtBin(mapped_bin[0], mapped_bin[1])

        mapped_doubleExtBin_weight = 0
        temp_bins = []
        for ii in range(len(mapped_doubleExtBin.bins)):
            for jj in range(len(mapped_doubleExtBin.bins[0])):
                b = mapped_doubleExtBin.bins[ii, jj]
                if (b.i, b.j) in self.bins_dict.keys():
                    mapped_doubleExtBin_weight += self.bins_dict[(b.i, b.j)].getWeight()
                    temp_bins.append(self.bins_dict[(b.i, b.j)])

        if mapped_doubleExtBin_weight > self.maxRS:

            logging.info('exact algo - new point may have changed the maxRS')
            x_min = (mapped_doubleExtBin.center[0] - Experiment_Setup.x_ratio) * self.bin_width
            x_max = (mapped_doubleExtBin.center[0] + 2 * Experiment_Setup.x_ratio) * self.bin_width
            y_min = (mapped_doubleExtBin.center[1] - Experiment_Setup.y_ratio) * self.bin_height
            y_max = (mapped_doubleExtBin.center[1] + 2 * Experiment_Setup.y_ratio) * self.bin_height

            temp_maxRS = self.exact_maxRS(t, temp_bins, x_min, x_max, y_min, y_max)
            if temp_maxRS > self.maxRS:
                self.maxRS = temp_maxRS
                self.setLastUpdate(t)

        return self.maxRS

class approx_MaxRS(Grid):

    def __init__(self):

        super().__init__()

        self.extBin = None
        self.extBin_weight = None
        self.last_update = None

    def setLastUpdate(self, t):
        self.last_update = t

    def approx_maxRS(self, t):
        self.update_all_bins_weights(t)
        self.extBin, self.extBin_weight = self.max_extBin_weight(t)
        self.setLastUpdate(t)
        return self.extBin, self.extBin_weight

    def update_approxMaxRS_NoEntry(self, t):
        self.update_all_bins_weights(t) # not necessary - can be removed
        self.update_extBin_weight(self.extBin, t)
        self.extBin_weight = self.weight_of_extBin(self.extBin)
        self.setLastUpdate(t)

    def update_approx_solution(self, point, t):

        mapped_bin = self.map_point_to_bin(point)
        candidate_extBins = Bin(mapped_bin[0], mapped_bin[1]).extBins_contain_bin()
        for b in candidate_extBins: self.update_extBin_weight(b, t)
        max_candidate_weight = max(candidate_extBins, key=lambda k: self.weight_of_extBin(k))

        self.update_approxMaxRS_NoEntry(t)

        if self.weight_of_extBin(max_candidate_weight) > self.extBin_weight:
            self.extBin_weight = self.weight_of_extBin(max_candidate_weight)
            self.extBin = max_candidate_weight
            logging.info('new point changed our maxRS')

        self.setLastUpdate(t)