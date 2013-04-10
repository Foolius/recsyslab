import numpy as np


class knn(object):
    def __init__(self, matrix, n):
        print("matrix")
        print(matrix)
        self.sim = np.zeros((matrix.shape[1], matrix.shape[1]))
        self.itemUserMatrix = matrix.transpose()
        print("itemuser")
        print(self.itemUserMatrix)
        self.computeCosSim()
        print("sim")
        print(self.sim)
        # self.sim = np.load("sim.data")
        self.recs = {}
        self.matrix = matrix

        order = self.sim.argsort(1)

        for j in xrange(0, self.sim.shape[1]):
            for i in xrange(0, self.sim.shape[1] - n):
                self.sim[j, order[j, i]] = 0
        print("ordered")
        print(self.sim)

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
        x = x.transpose()
#        print("x: %r"%x)
        for i in xrange(0, self.sim.shape[0]):
            if self.matrix[u, i] != 0:
                x[0, i] = 0

 #       print("0: %r"%x)
        order = x.argsort()
        s = set()
        for i in xrange(0, x.shape[0]):
            print("%r\t%r" % (x[0, i], order[0, i]))
        for i in xrange(0, n):
#            print("%r   %r" % (i, x[order[-i]]))
            s.add(x[0, order[0, -n]])

        print("\n")
        return s

    def getRecX(self, u, topN):
        vu = self.matrix[u]
        rec = vu * self.sim
        #sort desc
        return rec[0:n]
