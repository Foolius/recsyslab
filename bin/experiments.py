import util.reader
r = util.reader.stringSepReader("u.data", "\t")
internalID = r.getInternalUid("196")

import util.split
trainingDict, evaluationDict = util.split.split(r.getR(), 1234567890)

testMetricsList = []

import util.test
testMetricsList.append(util.test.hitrate)
testMetricsList.append(util.test.precision)
testMetricsList.append(util.test.f1)
testMetricsList.append(util.test.mrhr)
testMetricsList.append(util.test.auc)


recommenderList = []

import recommender.nonpersonalized
recommenderList.append(recommender.nonpersonalized.constant(
    trainingDict).getRec)
recommenderList.append(recommender.nonpersonalized.randomRec(
    trainingDict, 1234567890).getRec)

trainingMatrix, matrixEvaluationDict = (
    util.split.splitMatrix(r.getMatrix(), 123456789))

import recommender.knn
recommenderList.append(recommender.knn.itemKnn(trainingMatrix, 10).getRec)
recommenderList.append(recommender.knn.userKnn(trainingMatrix, 10).getRec)

import recommender.BPRMF
W, H = recommender.BPRMF.learnModel(r.getMaxUid(), r.getMaxIid(),
                                    0.01, 0.01, 0.01,
                                    # regularization parameter
                                    0.1,                # learning rate
                                    trainingDict,       # training dict
                                    150,                # number of features
                                    3,                  # number of epochs
                                    r.numberOfTransactions)

import recommender.mf
BPRMF = recommender.mf.MFrec(W, H, trainingDict)
recommenderList.append(BPRMF.getRec)

import recommender.RankMFX
W, H = recommender.RankMFX.learnModel(r.getMaxUid(), r.getMaxIid(),
                                      0.01, 0.01, 0.01,
                                      # regularization parameter
                                      0.1,              # learning rate
                                      trainingDict,     # training dict
                                      150,              # number of features
                                      3,                # number of epochs
                                      r.numberOfTransactions)

RankMFX = recommender.mf.MFrec(W, H, trainingDict)
recommenderList.append(RankMFX.getRec)

import recommender.svd
W, H = recommender.svd.learnModel(r.getMaxUid(), r.getMaxIid(),
                                  0.0002,         # learning rate
                                  trainingDict,   # training dict
                                  1000,           # number of features
                                  1,              # number of epochs
                                  1000)           # number of iterations

svd = recommender.mf.MFrec(W, H, trainingDict)
recommenderList.append(svd.getRec)

import recommender.slopeone
slopeone = recommender.slopeone.slopeone(trainingDict)
recommenderList.append(slopeone.getRec)

results = {}
for rec in recommenderList:
    results[rec] = {}
    for test in testMetricsList:
        results[rec][test] = -1


for rec in recommenderList:
    for test in testMetricsList:
        if not test.__name__ == 'auc':
            results[rec][test] = test(evaluationDict, rec, 10)
        else:
            results[rec][test] = test(evaluationDict, rec, r)

s = "recommender "
for test in testMetricsList:
    s += " & " + test.__name__
s += " \\\\\n"

for rec in recommenderList:
    s += type(rec.__self__).__name__
    for test in testMetricsList:
        s += " & " + str(results[rec][test])
    s += " \\\\\n"
