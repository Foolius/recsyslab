# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import util.reader
r = util.reader.stringSepReader("u.data", "\t")

# <codecell>

internalID = r.getInternalUid("196")
print(r.getR()[internalID])

# <codecell>

import util.split
trainingDict, evaluationDict = util.split.split(r.getR(), 1234567890)

# <codecell>

import recommender.nonpersonalized
constant = recommender.nonpersonalized.constant(trainingDict)
print(constant.getRec(0, 10))

# <codecell>

import util.helper
externalConstantgetRec = util.helper.getExternalRec(constant.getRec, r)
print(externalConstantgetRec("196", 10))

# <codecell>

import util.test
util.test.hitrate(evaluationDict, constant.getRec, 10)

# <codecell>

randomRec = recommender.nonpersonalized.randomRec(trainingDict, 12367890)
print(randomRec.getRec(0, 10))

# <codecell>

util.test.hitrate(evaluationDict, randomRec.getRec, 10)

# <codecell>

trainingMatrix, matrixEvaluationDict = (
    util.split.splitMatrix(r.getMatrix(), 123456789))

# <codecell>

import recommender.knn
userKnn = recommender.knn.userKnn(trainingMatrix, 10)

# <codecell>

util.test.hitrate(matrixEvaluationDict, userKnn.getRec, 10)

# <codecell>

import recommender.svd
W, H = recommender.svd.learnModel(r.getMaxUid(), r.getMaxIid(),
                                  0.0002,         # learning rate
                                  trainingDict,   # training dict
                                  770,            # number of features
                                  4,              # number of epochs
                                  1000)           # number of iterations

# <codecell>

import recommender.mf
svd = recommender.mf.MFrec(W, H, trainingDict)
util.test.hitrate(evaluationDict, svd.getRec, 10)

# <codecell>


