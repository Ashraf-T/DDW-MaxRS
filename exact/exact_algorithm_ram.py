from exact.hinterval import HInterval
from exact.interval import Interval
from exact.hline import HLine
import parameters
import numpy as np

class AlgorithmRAM:

    def __init__(self, input_set, space):
        self.input_set = input_set
        self.output_set = np.empty(0, dtype=HLine)
        self.space = space

    def exactMaxRS(self):
        return self.findMaxIntervals(self.input_set, self.output_set, self.space)

    def getOutputSet(self):
        return self.output_set

    def findMaxIntervals(self, src, dst, slab):

        if len(src) > 1e6:
            spanRectFile = np.empty(0, dtype=HInterval)
            slabs = np.empty(2, dtype=Interval)

            rectFiles = np.empty((2, 0))
            slabFiles = np.empty((2, 0))

            seperator = (slab.s + slab.e) / 2

            slabs[0] = Interval(slab.s, seperator, 0)
            slabs[1] = Interval(seperator, slab.e, 0)

            for hInv in src:
                for i in range(len(slabs)):
                    if hInv.getInv().isIntersect(slabs[i]):
                        if not slabs[i].isCovered(hInv.getInv()):
                            intersect = HInterval(hInv.getY(), hInv.getInv().getIntersect(slabs[i]))
                            rectFiles[i] = np.append(rectFiles[i], intersect)
                        else:
                            spanHInv = HInterval(hInv.getY(), Interval(slabs[i].s, slabs[i].e, hInv.getInv().weight))
                            print(spanHInv)
                            i += 1
                            while i < len(slabs) and slabs[i].isCovered(hInv.getInv()):
                                spanHInv.mergeWith(HInterval(hInv.getY(), Interval(slabs[i].s, slabs[i].e, hInv.getInv().weight)))
                                i += 1
                            spanRectFile = np.append(spanRectFile, spanHInv)
                            i -= 1

            for i in range(2):
                self.findMaxIntervals(rectFiles[i], slabFiles[i], slabs[i])
            return self.mergeSweep(dst, slabFiles, slabs, spanRectFile)

        elif len(src) > 0:
            intervals = np.empty(0, dtype=Interval)
            curMaxI = slab
            prevY = src[0].getY()
            intervals = np.append(intervals, slab)

            for hInv in src:
                if prevY != hInv.getY():
                    curMaxI = self.getMaxInterval(intervals)
                    dst = np.append(dst, HLine(prevY, curMaxI))
                    prevY = hInv.getY()

                intervalsNum = len(intervals)
                for i in range(intervalsNum):
                    inv = intervals[i]
                    if inv.isIntersect(hInv.getInv()):
                        intersect = inv.getWeightIntersect(hInv.getInv())
                        intervals[i] = intersect
                        if not inv.isCovered(hInv.getInv()):
                            for restInv in inv.getDiff(hInv.getInv()):
                                intervals = np.append(intervals, restInv)

                if hInv.getInv().weight < 0:
                    intervals = self.mergeIntervals(intervals)

            curMaxI = self.getMaxInterval(intervals)
            dst = np.append(dst, HLine(prevY, curMaxI))

        weights = [r.maxInv.weight for r in dst]

        return max(weights) if len(weights) > 0 else 0

    def mergeSweep(self, dstFile, slabFiles, slabs, upperFile):

        maxInvX = Interval(self.space.s, self.space.e, 0)
        maxInvY = Interval(parameters.ExactEnv.min, parameters.ExactEnv.max, 0)

        upcCounts = np.empty(2, dtype=int)
        curMaxInvs = np.empty(2, dtype=Interval)
        sweepLine = SweepingLineRam(slabFiles, upperFile)

        for i in range(len(curMaxInvs)):
            curMaxInvs[i] = slabs[i]

        prevY = parameters.ExactEnv.min
        pair = next(sweepLine.__iter__(), None)
        while not pair:
            r = pair[1]
            if isinstance(r, HLine):
                hLine = r
                slabIndex = pair[0]

                if prevY != parameters.ExactEnv.min and prevY != hLine.getY():
                    maxInv = self.getMaxInterval(curMaxInvs, upcCounts)
                    prevHLine = None
                    if np.array(dstFile).size:
                        prevHLine = dstFile[-1]
                    if (prevHLine is None) or (not prevHLine.getMaxI().equallsWithWeight(maxInv)):
                        insertedHLine = HLine(prevY, maxInv)
                        dstFile = np.append(dstFile, insertedHLine)

                        if maxInv.weight < maxInv.weight:
                            maxInvX = maxInv
                            maxInvY = Interval(prevY, parameters.ExactEnv.max, maxInv.weight)
                        elif maxInvX.weight > maxInv.weight and prevY < maxInvY.e:
                            maxInvY.e = prevY

                curMaxInvs[slabIndex] = hLine.getMaxInv()
                prevY = hLine.getY()

            elif isinstance(r, HInterval):
                hInv = r

                if prevY != parameters.ExactEnv.min and prevY != hInv.getY():
                    maxInv = self.getMaxInterval(curMaxInvs, upcCounts)
                    prevHLine = None

                    if np.array(dstFile).size:
                        prevHLine = dstFile[- 1]
                    if (prevHLine is None) or (not prevHLine.getMaxI().equalWithWeight(maxInv)):
                        insertedHLine = HLine(prevY, maxInv)
                        dstFile = np.append(dstFile, insertedHLine)

                        if maxInvX.weight < maxInv.weight:
                            maxInvX = maxInv
                            maxInvY = Interval(prevY, self.space.e, maxInv.weight)
                        elif maxInvX.weight > maxInv.weight and prevY < maxInvY.e:
                            maxInvY.e = prevY

                for i in range(2):
                    if slabs[i].isCovered(hInv.getInv()):
                        upcCounts[i] += hInv.getInv().weight
                prevY = hInv.getY()

            pair = sweepLine.next()

        return maxInvX.weight
        # return Rectangle.fromPointsWithWeight(Point(maxInvX.s, maxInvY.s, 0), Point(maxInvX.e, maxInvY.e, 0), maxInvX.weight)

    def mergeIntervals(self, intervals):
        i, j = 0, 0
        while i < len(intervals):
            while j < len(intervals):
                if i != j and intervals[i].isMergeable(intervals[j]):
                    intervals[i].mergeWith(intervals[j])
                    intervals = np.delete(intervals, j)
                else:
                    j += 1
            i += 1

        return intervals

    def getMaxInterval(self, intervals):
        maxI = None
        for inv in intervals:
            if ((not isinstance(maxI, Interval)) and maxI is None) or (isinstance(maxI, Interval) and  (maxI.weight < inv.weight)):
                maxI = inv
            elif maxI.weight == inv.weight and maxI.isAdjacent(inv):
                maxI.mergeWith(inv)
        return maxI

class SweepingLineIterator:

    def __init__(self, sweepingLine):
        self.sweepingLine = sweepingLine
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        bottom = None
        i = -1
        maxIndex = -1
        for i in range(len(self.sweepingLine.curHLines)):
            if (self.sweepingLine.curHLines[i] != None) and ((bottom == None) or (HLine(bottom).getY() > self.sweepingLine.curHLines[i].getY())):
                bottom = self.sweepingLine.curHLines[i]
                maxIndex = i

        if (self.sweepingLine.upperHInv != None) and ((maxIndex < 0) or (HLine(bottom).getY() > self.sweepingLine.upperHInv.getY())):
            bottom = self.sweepingLine.upperHInv
            maxIndex = -1
            self.sweepingLine.upperHInv = self.upperFile_iter.next()
        else:
            self.sweepingLine.curHLines[maxIndex] = self.sweepingLine.slabFile_iters[maxIndex] if not self.sweepingLine.slabFile_iters[maxIndex] else None

        return (maxIndex, bottom)

class SweepingLineRam:

    def __init__(self, slabFiles, upperFile):
        self.slabFiles = slabFiles
        self.upperFile = upperFile
        self.curHLines = np.empty(len(slabFiles), dtype=HLine)

        self.upperFile_iter = None if not np.array(self.upperFile).size else np.nditer(self.upperFile)
        self.slabFile_iters = np.empty(2, dtype=np.nditer)

        self.upperHInv = None if not np.array(self.upperFile).size else self.upperFile_iter.next()
        for i in range(len(self.curHLines)):
            self.slabFile_iters[i] = None if not np.array(self.slabFiles[i]).size else np.nditer(self.slabFiles[i])
            self.curHLines[i] = None if not np.array(self.slabFiles[i]).size else self.slabFile_iters[i].next()

    def __iter__(self):
        return SweepingLineIterator(self)
