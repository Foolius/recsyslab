import helper
import numpy as np


class tabSepReader(object):

    def __init__(self, filename):
        self.R = {}
        self.uidDict = helper.idOrigDict()
        self.iidDict = helper.idOrigDict()
        self.dbfile = open(filename, 'r')
        self.numberOfTransactions = 0

        print("Start reading the database.")
        for line in self.dbfile:
            self.numberOfTransactions += 1
            split = line.strip().split("\t", 3)
            origUid = split[0]
            origIid = split[1]
            rating = int(split[2])

            if self.numberOfTransactions % 10000 == 0:
                print("%r Lines read." % self.numberOfTransactions)

            uid = self.uidDict.add(origUid)
            iid = self.iidDict.add(origIid)

            # put in R when not already there
            if uid in self.R:
                self.R[uid].add((iid, rating))
            else:
                self.R[uid] = {(iid, rating)}

        self.matrix = np.matrix(np.zeros((
            self.getMaxUid() + 1, self.getMaxIid() + 1)))
        for u in self.R.iterkeys():
            for d in self.R[u]:
                item = d[0]
                rating = d[1]
                self.matrix[u, item] = 1

    def getR(self):
        return self.R

    def getMatrix(self):
        """user x items"""
        print self.matrix.shape
        return self.matrix

    def getOriginalUid(self, uid):
        return self.uidDict.getOrig(uid)

    def getOriginalIid(self, iid):
        return self.iidDict.getOrig(iid)

    def getMaxIid(self):
        return self.iidDict.id - 1

    def getMaxUid(self):
        return self.uidDict.id - 1
