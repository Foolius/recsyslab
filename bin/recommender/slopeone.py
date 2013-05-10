class slopeone(object):
    def __init__(self, R):
        self.diffs = {}
        self.R = R

        for u in R.keys():
            for i, r in R[u]:
                if not i in self.diffs:
                    self.diffs[i] = {}

                for i1, r1 in R[u]:
                    if i == i1:
                        continue
                    if not i1 in self.diffs[i]:
                        self.diffs[i][i1] = [0.0, 0.0]

                    self.diffs[i][i1][0] += r - r1
                    self.diffs[i][i1][1] += 1

    def getRec(self, u, n):
        maxIid = max(self.diffs.keys())
        userItems = [x[0] for x in self.R[u]]
        predictionList = []

        for i in xrange(0, maxIid + 1):
            if i in userItems:
                continue

            ratingSum = 0
            count = 0
            for i1, r in self.R[u]:
                if i in self.diffs:
                    if i1 in self.diffs[i]:
                        ratingSum += (r + (self.diffs[i][i1][0] /
                                           self.diffs[i][i1][1])
                                      ) * self.diffs[i][i1][1]
                        count += self.diffs[i][i1][1]

            if count == 0:
                continue
            ratingSum /= count
            predictionList.append((i, ratingSum))

        import helper
        sortedList = helper.sortList(predictionList)

        if n > len(sortedList) or n == -1:
            return sortedList
        return sortedList[:n]
