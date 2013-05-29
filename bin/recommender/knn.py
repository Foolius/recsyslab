"""Two classes for k-Nearest-Neighbor(knn) recommendation.

    itemKnn --  Item based knn
    userKnn --  User based knn

    Based on "Evaluation of Item-Based Top-N Recommendation Algortihms"
    by George Karypis.
"""
import numpy as np


class itemKnn(object):
    """Class for item based knn."""

    def __init__(self, userItemMatrix, n):
        """Builds a model for Item based knn.

            userItemMatrix  --  A matrix where an entry at i, j is the rating
                                the ith user gave the jth item.
            n               --  number of neighbors which are getting computed.

        Uses the cosine for similarity."""

        self.itemUserMatrix = userItemMatrix.transpose()
        self.sim = np.zeros((userItemMatrix.shape[1], userItemMatrix.shape[1]))
        self.sim = computeCosSim(self.sim, self.itemUserMatrix)
        self.userItemMatrix = userItemMatrix

        if n > self.sim.shape[0]:
            n = self.sim.shape[0]

        order = self.sim.argsort(1)

        # for each row in sim:
        # Set all entries to 0 except the n highest
        for j in xrange(0, self.sim.shape[1]):
            for i in xrange(0, self.sim.shape[1] - n):
                self.sim[j, order[j, i]] = 0

    def getRec(self, u, n):
        """Returns the n best recommendations for user u.

        Set n = -1 to get all items recommended"""
        if n > self.userItemMatrix.shape[1] or n == -1:
            n = self.userItemMatrix.shape[1]

        # x are the similarities of each item to the items u bought
        # w.r.t. only the highest n similarities are saved.
        x = self.userItemMatrix[u] * self.sim

        # Throw out items the user already purchased
        for i in xrange(0, self.sim.shape[0]):
            if self.userItemMatrix[u, i] != 0:
                x[0, i] = 0

        order = x.argsort()
        l = []
        for i in xrange(1, n + 1):
            l.append(order[0, -i])
        return l


class userKnn(object):
    def __init__(self, userItemMatrix, n):
        """Builds a model for user based knn.

            userItemMatrix  --  A matrix where an entry at i, j is the rating
                                the ith user gave the jth item.
            n               --  number of neighbors which get computed.

        Uses the cosine for similarity."""
        self.userItemMatrix = userItemMatrix
        self.sim = np.zeros((userItemMatrix.shape[0], userItemMatrix.shape[0]))
        self.sim = computeCosSim(self.sim, self.userItemMatrix)

        if n > self.sim.shape[0]:
            n = self.sim.shape[0]

        order = self.sim.argsort(1)

        # for each row in sim:
        # Set all entries to 0 except the n highest
        for j in xrange(0, self.sim.shape[1]):
            for i in xrange(0, self.sim.shape[1] - n):
                self.sim[j, order[j, i]] = 0

    def getRec(self, u, n):
        """Returns the n best recommendations for user u.

        Set n = -1 to get all items recommended"""
        if n > self.userItemMatrix.shape[1] or n == -1:
            n = self.userItemMatrix.shape[1]

        # x is the weighted sum of the items
        # weighted with the similarity between u and the
        # other users.
        x = self.sim[u] * self.userItemMatrix

        for i in xrange(0, self.sim.shape[0]):
            if self.userItemMatrix[u, i] != 0:
                x[0, i] = 0

        order = x.argsort()
        l = []
        for i in xrange(1, n + 1):
            l.append(order[0, -i])

        return l


def computeCosSim(sim, matrix):
    """
    Computes the cos of every two lines in the matrix and writes them into sim.
    """
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
    """Gets two vectors(onedimensional np.matrix) and computes their cosine."""
    dotproduct = np.dot(a.getA()[0], b.getA()[0])
    if dotproduct == 0:
        return 0

    normproduct = np.linalg.norm(a) * np.linalg.norm(b)
    if normproduct == 0:
        return 0

    return dotproduct / normproduct
