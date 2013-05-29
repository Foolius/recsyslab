import util.reader
r = util.reader.stringSepReader("u.data", "\t")
internalID = r.getInternalUid("196")
print(r.getR()[internalID])

import util.split
trainingDict, evaluationDict = util.split.split(r.getR(), 1234567890)
trainingMatrix, matrixEvaluationDict = (
    util.split.splitMatrix(r.getMatrix(), 123456789))

import recommender.nonpersonalized
constant = recommender.nonpersonalized.constant(r.getR())
print(constant.getRec(0, 10))

import util.helper
externalConstantgetRec = util.helper.getExternalRec(constant.getRec, r)
print(externalConstantgetRec("196", 10))
