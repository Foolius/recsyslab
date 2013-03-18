import evaluation
import reader
import baselines
import test
import helper
import bprmf
import numpy as np
import RankMFX

r=reader.tabSepReader("u.data")

trainingDict,testDict=evaluation.split(r.getR())

#helper.writeInternalToFile(r,trainingDict,"training")
#helper.writeInternalToFile(r,testDict,"test")

#rec=baselines.randomRec(trainingDict)
#print test.hitrate(testDict, rec.getRec,10)

W,H = bprmf.learnModel(r.getMaxUid(),r.getMaxIid(),0.1,0.1,0.1,0.1,trainingDict,10, 10,
					r.numberOfTransactions)

rec=test.svdtest(W,H)

print test.hitrate(testDict,rec.getRec,10)
