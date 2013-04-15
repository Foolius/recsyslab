import helper
import numpy as np


def hitrate(testR, recommender, n):
    hits = 0.0
    items = 0.0
    for u in testR.iterkeys():
        if u % 100 == 0:
            print("%r users tested" % u)
            print("Hits so far: %r" % hits)
        recs = recommender(u, n)
        if len(recs) > n and not n == -1:
            print("Fatal error: too much recommended items.")
        for i in testR[u]:
            if i in recs:
                hits += 1
            items += 1

    print("Number of hits: %r" % hits)
    print("Number of possible hits: %r" % items)
    print("Hitrate: %r" % (hits / items))
    return hits / items


def mrhr(testR, recommender, n):
    score = 0.0
    items = 0.0
    for u in testR.iterkeys():
        if u % 100 == 0:
            print("%r users tested" % u)
            print("Score so far: %r" % score)

        recs = recommender(u, n)
        if len(recs) > n and not n == -1:
            print("Fatal error: too much recommended items.")

        for i in testR[u]:
            if i in recs:
                score += 1.0 / (recs.index(i) + 1)
            items += 1

    print("Score: %r" % score)
    print("Number of possible hits: %r" % items)
    print("Mean Reciprocal Hitrate: %r" % (score / items))
    return score / items


def auc(testR, recommender, r):
    """Returns the AUC of the recommender function.
    See BPR paper."""
    maxIid = r.getMaxIid()

    result = 0
    for u in testR.iterkeys():
        if u % 100 == 0:
            print("%r users tested" % u)
            print("Score so far: %r" % result)
        e = 0.0  # number of items in E
        score = 0  # how often is the hidden item better
        recs = recommender(u, -1)
        for i in testR[u]:
            for j in xrange(0, maxIid):
                if j in r.getR()[u] or j == i or not j in recs:
                    continue
                e += 1
                if recs.index(i) > recs.index(j):
                    score += 1
        result += score / e
    result /= len(testR.keys())
    print("AUC: %r" % result)
    return result


class MFtest(object):

    def __init__(self, W, H, trainingR):
        self.W = W
        self.H = H
        self.R = trainingR

    def getRec(self, u, n):
        scoredict = {}
        for i in range(0, self.H.shape[0]):
            if not i in self.R[u]:
                scoredict[i] = np.dot(self.W[u], self.H[i])

        return helper.sortList(scoredict.iteritems())[:n]
