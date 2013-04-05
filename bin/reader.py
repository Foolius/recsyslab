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
            split = line.strip().split()
            origUid = split[0]

            if self.numberOfTransactions % 10000 == 0:
                print("%r Lines read." % self.numberOfTransactions)

            origIid = split[1]
            uid = self.uidDict.add(origUid)
            iid = self.iidDict.add(origIid)

            # put in R when not already there
            if uid in self.R:
                self.R[uid].add(iid)
            else:
                self.R[uid] = {iid}

        self.matrix = np.matrix(np.zeros((self.getMaxUid(), self.getMaxIid())))
        for u in self.R.iterkeys():
            for i in self.R[u]:
                self.matrix[u, i] = 1.0

    def getR(self):
        return self.R

    def getMatrix(self):
        """user x items"""
        return self.matrix

    def getOriginalUid(self, uid):
        return self.uidDict.getOrig(uid)

    def getOriginalIid(self, iid):
        return self.iidDict.getOrig(iid)

    def getMaxIid(self):
        return self.iidDict.id

    def getMaxUid(self):
        return self.uidDict.id
