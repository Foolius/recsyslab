import util.reader
r = util.reader.stringSepReader("u.data", "\t")
internalID = r.getInternalUid("196")
print(r.getR()[internalID])

import util.split
trainingDict, evaluationDict = util.split.split(r.getR(), 1234567890)

import recommender.nonpersonalized
constant = recommender.nonpersonalized.constant(r.getR())
print(constant.getRec(0, 10))

import util.helper
externalConstantgetRec = util.helper.getExternalRec(constant.getRec, r)
print(externalConstantgetRec("196", 10))

import util.test
util.test.hitrate(evaluationDict, constant.getRec, 10)

util.test.precision(evaluationDict, constant.getRec, 10)

util.test.f1(evaluationDict, constant.getRec, 10)

util.test.mrhr(evaluationDict, constant.getRec, 10)

util.test.auc(evaluationDict, constant.getRec, r)

randomRec = recommender.nonpersonalized.randomRec(r.getR(), 12367890)
print(randomRec.getRec(0, 10))
util.test.hitrate(evaluationDict, randomRec.getRec, 10)

trainingMatrix, matrixEvaluationDict = (
    util.split.splitMatrix(r.getMatrix(), 123456789))

# import recommender.knn
# itemKnn = recommender.knn.itemKnn(trainingMatrix, 10)

# util.test.hitrate(matrixEvaluationDict, itemKnn.getRec, 10)

# userKnn = recommender.knn.userKnn(trainingMatrix, 10)

# util.test.hitrate(matrixEvaluationDict, userKnn.getRec, 10)

import recommender.BPRMF
W, H = recommender.BPRMF.learnModel(r.getMaxUid(), r.getMaxIid(),
                                    0.01, 0.01, 0.01,   # regularization parameter
                                    0.1,                # learning rate
                                    trainingDict,       # training dict
                                    150,                # number of features
                                    0,                  # number of epochs
                                    r.numberOfTransactions)

import recommender.mf
BPRMF = recommender.mf.MFrec(W, H, trainingDict)
#util.test.hitrate(evaluationDict, BPRMF.getRec, 10)

import recommender.RankMFX
W, H = recommender.RankMFX.learnModel(r.getMaxUid(), r.getMaxIid(),
                                      0.01, 0.01, 0.01, # regularization parameter
                                      0.1,              # learning rate
                                      trainingDict,     # training dict
                                      150,              # number of features
                                      0,                # number of epochs
                                      r.numberOfTransactions)

BPRMF = recommender.mf.MFrec(W, H, trainingDict)
#util.test.hitrate(evaluationDict, BPRMF.getRec, 10)

import recommender.svd
W, H = recommender.svd.learnModel(r.getMaxUid(), r.getMaxIid(),
                                  0.0002,         # learning rate
                                  trainingDict,   # training dict
                                  1000,           # number of features
                                  1,              # number of epochs
                                  1000)           # number of iterations

svd = recommender.mf.MFrec(W, H, trainingDict)
util.test.hitrate(evaluationDict, svd.getRec, 10)
