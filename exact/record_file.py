from exact.env import Env
from point import Point
from exact.hinterval import HInterval
from exact.interval import Interval
from exact.hline import HLine
import os

class BlockFile:

    def __init__(self, fname):

        self.name = fname
        if not os.path.exists(self.name):
            with open(self.name, 'w'): pass
        with open(self.name, 'r') as self.fp:
            self.records = [line for line in self.fp.readlines() if len(line.split())>0]
        self.records_num = len(self.records)

    def read(self):
        Env.RecordCount += 1
        return self.records[Env.RecordCount - 1]

    def setNumOfRecords(self, recordsNum):
        self.records_num = recordsNum


class RecordIterator:

    def __init__(self, recordFile):

        self.recordFile = recordFile
        self.index = 0

    def __next__(self):
        if self.index < self.recordFile.disk.records_num:
            result = self.recordFile.disk.records[self.index]
            self.index += 1
            return result
        raise StopIteration

class RecordFile:

    def __init__(self, fname):

        self.fname = fname
        self.disk = BlockFile(self.fname)
        self.recordsNum = self.disk.records_num
        self.curRecordNo = 0

    def empty(self):
        return self.recordsNum == 0

    def clear(self):
        self.recordsNum = 0
        self.disk.setNumOfRecords(0)
        # self.disk = []

    def getCurrentRecordNo(self):
        return self.curRecordNo

    def getNumofRecords(self):
        return self.recordsNum

    def insert(self, e, no=None):
        if no == None:
            self.disk.records.append(e)
            self.recordsNum += 1
        elif no < self.recordsNum:
            self.disk.records[no] = e

    def close(self):
        with open(self.fname, 'w') as file:
            for r in self.disk.records:
                file.write(str(r)+'\n')

    def __iter__(self):
        return RecordIterator(self)

class PointFile(RecordFile):

    def __init__(self, fname):
        super().__init__(fname)

    def get(self, no):
        p = list(self.disk.records[no].split())
        return Point(float(p[0]), float(p[1]), float(p[2]), float(p[3]), float(p[4]))


class HInvFile(RecordFile):

    def __init__(self, fname):
        super().__init__(fname)

    def get(self, no):
        rec = list(self.disk.records[no].split())
        inv = Interval(float(rec[1]), float(rec[2]), float(rec[3]))
        return HInterval(float(rec[0]), inv)

    def ramSort(self):

        invList = [self.disk.records[i] for i in range(self.recordsNum)]
        invList_sorted = sorted(invList)

        for i in range(len(invList_sorted)):
            self.insert(invList_sorted[i], i)

class InvFile(RecordFile):

    def __init__(self, fname):
        super().__init__(fname)

    def get(self, no):
        rec = list(self.disk.records[no].split())
        return Interval(float(rec[1]), float(rec[2]), float(rec[3]))

    def ramSort(self):

        invList = [self.disk.records[i] for i in range(self.recordsNum)]
        invList_sorted = sorted(invList)

        for i in range(len(invList_sorted)):
            self.insert(invList_sorted[i], i)

class HLineFile(RecordFile):

    def __init__(self, fname):
        super().__init__(fname)

    def get(self, no):
        rec = list(self.disk.records[no].split())
        inv = Interval(float(rec[1]), float(rec[2]), float(rec[3]))
        return HLine(float(rec[0]), inv)
