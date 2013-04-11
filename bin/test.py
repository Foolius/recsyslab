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
        if len(recs) > n:
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
        if len(recs) > n:
            print("Fatal error: too much recommended items.")

        for i in testR[u]:
            if i in recs:
                score += 1.0 / (recs.index(i) + 1)
            items += 1

    print("Score: %r" % score)
    print("Number of possible hits: %r" % items)
    print("Mean Reciprocal Hitrate: %r" % (score / items))
    return score / items


def auc(testR, recommender, n, trainingDict):
    """Returns the AUC of the recommender function.
    See BPR paper."""
    i = testR[u]

    for u in testR.iterkeys():



class MFtest(object):

    def __init__(self, W, H, trainingR):
        self.W = W
        self.H = H
        self.R = trainingR
        # print(self.R)

    def getRec(self, u, n):
        scoredict = {}
        for i in range(0, self.H.shape[0]):
            if not i in self.R[u]:
                scoredict[i] = np.dot(self.W[u], self.H[i])

        return helper.sortList(scoredict.iteritems())[:n]
