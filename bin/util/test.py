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
        if len(recs) != n and not n == -1:
            print("Fatal error: not the right number of items.")
        testSet = set()
        for t in testR[u]:
            testSet.add(t[0])
        hits += len(testSet.intersection(set(recs)))
        items += len(testSet)

    print("Number of hits: %r" % hits)
    print("Number of possible hits: %r" % items)
    print("Hitrate: %r" % (hits / items))
    return hits, items


def precision(testR, recommender, n):
    hits = hitrate(testR, recommender, n)[0]
    if n == 0:
        return 0
    return hits / n


def f1(testR, recommender, n):
    hits, items = hitrate(testR, recommender, n)
    recall = hits / items
    if recall == 0:
        return 0

    prec = hits / n

    result = ((2 * recall * prec) /
              (recall + prec))
    print("F1: %r" % result)
    return result


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

        testSet = set()
        for t in testR[u]:
            testSet.add(t[0])

        for i in testSet:
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
            score += r.getMaxIid() - recs.index(i[0]) - 1
            e += maxIid - 1
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
#            if not i in self.R[u]:
            if not i in [x[0] for x in self.R[u]]:
                scoredict[i] = np.dot(self.W[u], self.H[i])
#            else:
#                print "i in R[u]", i ,u
#        print u,scoredict
#        import time
#        time.sleep(4)

        return helper.sortList(scoredict.iteritems())[:n]
