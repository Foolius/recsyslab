"""Contains a class to manage a database."""
import helper
import numpy as np


class stringSepReader(object):
    """A class to manage a database."""

    def __init__(self, filename, separator):
        """Reads in a database file.

        The lines of the database file have to look like this:
            UserID<separator>ItemID<separator>Rating
        If there is just an UserID and an ItemID the rating is set to 1.
        Everything coming after the rating will be ignored,
        but when omit the rating and still have something following the ItemID
        this will be understood as the rating."""
        self.R = {}
        self.uidDict = helper.idOrigDict()
        self.iidDict = helper.idOrigDict()
        self.dbfile = open(filename, 'r')
        self.numberOfTransactions = 0

        print("Start reading the database.")
        for line in self.dbfile:
            self.numberOfTransactions += 1
            split = line.strip().split(separator, 3)
            origUid = split[0]
            origIid = split[1]
            try:
                rating = int(float(split[2]))
            except IndexError:
                rating = 1

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
                self.matrix[u, item] = rating

    def getR(self):
        """Return the database as a dict.

        The dict has internal UserIDs as keys and
        (ItemID, Rating) Tuples as values"""
        return self.R

    def getMatrix(self):
        """Get the database as a matrix.

        The lines of the matrix are corresponding to the users
        and the columns to the items.
        So the n,m entry is the rating the nth user gave the mth item."""
        return self.matrix

    def getOriginalUid(self, internalUid):
        """Maps the given internal UserID to the corresponding original UserID.
        """
        return self.uidDict.getOrig(internalUid)

    def getOriginalIid(self, internalIid):
        """Maps the given internal ItemID to the corresponding original ItemID.
        """
        return self.iidDict.getOrig(internalIid)

    def getInternalUid(self, originalUid):
        """Maps the given original UserID to the corresponding internal UserID.

        The passed original UserID has to be a string.
        """
        return self.uidDict.getId(originalUid)

    def getInternalIid(self, originalIid):
        """Maps the given original ItemID to the corresponding internal ItemID.

        The passed original UserID has to be a string.
        """
        return self.iidDict.getId(originalIid)

    def getMaxIid(self):
        """Returns the highest internal assigned ItemID."""
        return self.iidDict.id - 1

    def getMaxUid(self):
        """Returns the highest internal assigned UserID."""
        return self.uidDict.id - 1
