import numpy as np


class knn(object):
    def __init__(self, matrix, n):
        self.sim = np.zeros((matrix.shape[1], matrix.shape[1]))
        self.itemUserMatrix = matrix.transpose()
        self.computeCosSim()
        # self.sim = np.load("sim.data")
        self.recs = {}
        self.matrix = matrix

        order = self.sim.argsort(1)

        for j in xrange(0, self.sim.shape[1]):
            for i in xrange(0, self.sim.shape[1] - n):
                self.sim[0, order[0, i]] = 0

        self.normRow(self.itemUserMatrix)

    def computeCosSim(self):
        count = 0
        for i in xrange(1, self.sim.shape[1]):
            if count % 100 == 0:
                print("%r Similarities calculated" % count)
            count += 1

            for j in xrange(0, i):
                if i == j:
                    self.sim[i, j] = 0
                else:
                    self.sim[i, j] = self.sim[j, i] = self.cos(
                        self.itemUserMatrix[i], self.itemUserMatrix[j])

    def cos(self, a, b):
        """gets two vectors(onedimensional np.matrix)
        and computes their cosine"""
        dotproduct = np.dot(a.getA()[0], b.getA()[0])
        if dotproduct == 0:
            return 0

        normproduct = np.linalg.norm(a) * np.linalg.norm(b)
        if normproduct == 0:
            return 0

        return dotproduct / normproduct

    def computeCondProbSim(self):
        count = 0
        for i in xrange(0, self.sim.shape[1]):
            if count % 100 == 0:
                print("%r Similarities calculated" % count)
            count += 1

            for j in xrange(0, self.sim.shape[1]):
                if i == j:
                    self.sim[i, j] = 0
                else:
                    self.sim[i, j] = self.cos(
                        self.itemUserMatrix[i], self.itemUserMatrix[j])

    def condProb(a, b):
        """Returns the similarity of a and b."""
        fa = a.sum()
        if fa == 0:
            return 0
        fb = b.sum()
        if fb == 0:
            return 0

    def normRow(self, m):
        "Normalize each row of the matrix so the sum is 1"
        for i in xrange(0, m.shape[0]):
            m[i] /= np.sum(m[0])

    def getRec(self, u, n):
        """Returns the n best recommendations for user u"""

#        print("u: %r"%self.matrix[u])
        x = self.sim * self.matrix[u].transpose()
#        print("x: %r"%x)
        for i in xrange(0, self.sim.shape[0]):
            if not self.matrix[u, i] == 0:
                x[i] = 0

 #       print("0: %r"%x)
        order = x.argsort()
        for i in xrange(0, self.sim.shape[1] - n):
            x[order[i]] = 0

  #      print("r: %r"%x)
   #     time.sleep(4)
        s = set()
        for i in xrange(0, self.sim.shape[1]):
            if not x[i] == 0:
                s.add(i)

        return s
