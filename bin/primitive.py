import random
import helper


class constant(object):

    def __init__(self, dbdict):
        self.dictionary = {}
        self.sortedList = []
        for data in dbdict.iteritems():
            for itemRating in iter(data[1]):
                item = itemRating[0]
                if item in self.dictionary:
                    self.dictionary[item] += 1
                else:
                    self.dictionary[item] = 1

       self.sortedList = helper.sortList(self.dictionary.iteritems())

    def getRec(self, user, n):
        if len(self.sortedList) < n or n == -1:
            n = len(self.sortedList)
        return self.sortedList[:n]


class randomRec(object):
    def __init__(self, dbdict):
        self.maxIid = 0
        for data in dbdict.iteritems():
            for itemRating in iter(data[1]):
                item = itemRating[0]
                if item > self.maxIid:
                    self.maxIid = item
        self.maxIid += 1

    def getRec(self, user, n):
        random.seed(1234567890)
        if self.maxIid < n or n == -1:
            l = range(self.maxIid)
            random.shuffle(l)
            return l
        return list(random.sample(range(self.maxIid), n))
