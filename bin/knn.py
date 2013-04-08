import numpy as np
import helper


class knn(object):
    def __init__(self, matrix, n):
        self.sim = np.zeros((matrix.shape[1], matrix.shape[1]))
        self.itemUserMatrix = matrix.transpose()
        #self.computeSim()
        self.sim = np.load("sim.data")
        self.recs = {}

        #self.sim.dump("sim.data")

        order = self.sim.argsort(1)

        for j in xrange(0, self.sim.shape[1]):
            self.recs[j] = set()
            for i in xrange(0, self.sim.shape[1] - 10):
                self.sim[0, order[0, i]] = 0
            for i in xrange(order.shape[0] - 10, self.sim.shape[1]):
                self.recs[j].add(i)

        self.normRow(self.itemUserMatrix)

    def computeSim(self):
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

    def normRow(self, m):
        "Normalize each row of the matrix so the sum is 1"
        for i in xrange(0, m.shape[0]):
            m[i] /= np.sum(m[0])

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

    def getRec(self, u, n):
        """Returns the n best recommendations for user u"""
        if not len(self.recs[u]) == 10:
            print(len(self.recs[u]))
        return self.recs[u]

        U = set()  # items the user bought
        C = set()  # items similar to the items of u
        for j in xrange(0, self.sim.shape[1]):
            if self.itemUserMatrix[j, u]:
                U.add(j)
                C = C.union(self.mostSim(j, n))

        C.difference_update(U)
        l = []
        for c in C:
            l.append((c, self.simToSet(U, c, n)))

        return helper.listToSet(helper.sortList(l), n)

    @helper.cache
    def mostSim(self, item, n):
        """Returns the n most similar items for item."""
        scorelist = []
        for i in xrange(self.sim.shape[0]):
            if i == item:
                continue
            scorelist.append((i, self.sim[item, i]))
        return helper.listToSet(helper.sortList(scorelist), n)

    def simToSet(self, itemSet, item, n):
        """Returns the sum of the similarities of itemSet and item.
        not exactly like in the paper because I'm adding up all items
        in the set and not only n."""
        simsum = 0.0
        for s in itemSet:
            if item in self.mostSim(s, n):
                simsum += self.sim[s, item]
        return simsum
