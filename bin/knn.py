import numpy as np


class itemKnn(object):
    def __init__(self, userItemMatrix, n):
        self.itemUserMatrix = userItemMatrix.transpose()
        self.sim = np.zeros((userItemMatrix.shape[1], userItemMatrix.shape[1]))
        self.sim = computeCosSim(self.sim, self.itemUserMatrix)
        self.userItemMatrix = userItemMatrix

        if n > self.sim.shape[0]:
            n = self.sim.shape[0]

        order = self.sim.argsort(1)

        for j in xrange(0, self.sim.shape[1]):
            for i in xrange(0, self.sim.shape[1] - n):
                self.sim[j, order[j, i]] = 0

    def getRec(self, u, n):
        """Returns the n best recommendations for user u"""

        if n > self.sim.shape[0]:
            n = self.sim.shape[0]

        x = self.userItemMatrix[u] * self.sim

        for i in xrange(0, self.sim.shape[0]):
            if self.userItemMatrix[u, i] != 0:
                x[0, i] = 0

        order = x.argsort()
        l = []
        for i in xrange(1, n + 1):
            l.append(order[0, -i])

        return l


def computeCosSim(sim, matrix):
    count = 0
    for i in xrange(1, sim.shape[1]):

        for j in xrange(0, i):
            if count % 10000 == 0:
                print("%r Similarities calculated" % count)
            count += 1
            sim[i, j] = sim[j, i] = cos(
                matrix[i], matrix[j])
    return sim


def cos(a, b):
    """gets two vectors(onedimensional np.matrix)
    and computes their cosine"""
    dotproduct = np.dot(a.getA()[0], b.getA()[0])
    if dotproduct == 0:
        return 0

    normproduct = np.linalg.norm(a) * np.linalg.norm(b)
    if normproduct == 0:
        return 0

    return dotproduct / normproduct


def computeCondProbSim(sim, itemUserMatrix):
    count = 0
    for i in xrange(0, sim.shape[1]):
        for j in xrange(0, sim.shape[1]):
            if count % 10000 == 0:
                print("%r Similarities calculated" % count)
            count += 1

            if i == j:
                sim[i, j] = 0
            else:
                sim[i, j] = condProb(
                    itemUserMatrix[i], itemUserMatrix[j])


def condProb(a, b):
    """Returns the similarity of a and b."""
    fa = a.sum()
    if fa == 0:
        return 0
    fb = b.sum()
    if fb == 0:
        return 0
