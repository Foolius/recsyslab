""""Two non-personalized algorithms to compare the results.

    constant    --  recommends the overall most popular items.
    randomRec   --  recommends randomly
    """
import random
from util import helper


class constant(object):
    """Recommends the most popular.

    So there is no personalization and the recommendations are the same for
    each user.
    """
    def __init__(self, dbdict):
        """Initialize the class.

            dbdict  --  A dict of the form UserID -> (ItemId, Rating)
        """
        self.dictionary = {}
        self.sortedList = []
        for data in dbdict.iteritems():
            for item, rating in iter(data[1]):
                if item in self.dictionary:
                    self.dictionary[item] += rating
                else:
                    self.dictionary[item] = rating

        self.sortedList = helper.sortList(self.dictionary.iteritems())

    def getRec(self, user, n):
        """Recommends n items for user n, which is obsolete in this case.

        Set n = -1 to get all items recommended"""
        if len(self.sortedList) < n or n == -1:
            n = len(self.sortedList)
        return self.sortedList[:n]


class randomRec(object):
    """Recommends items randomly."""

    def __init__(self, dbdict, seed):
        """Initialize the class.

            dbdict  --  A dict of the form UserID -> (ItemId, Rating)
            seed    --  The seed for the randomness
        """
        self.maxIid = 0
        self.seed = seed
        for data in dbdict.iteritems():
            for itemRating in iter(data[1]):
                item = itemRating[0]
                if item > self.maxIid:
                    self.maxIid = item
        self.maxIid += 1

    def getRec(self, user, n):
        """
        Recommends n random items for user n, which is obsolete in this case.

        Set n = -1 to get all items recommended"""
        random.seed(self.seed)
        if self.maxIid < n or n == -1:
            l = range(self.maxIid)
            random.shuffle(l)
            return l
        return list(random.sample(range(self.maxIid), n))
