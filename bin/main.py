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

#rec=baselines.constant(trainingDict)
#print test.hitrate(testDict, rec.getRec,10)
rank=RankMFX.RankMFX()
W,H = rank.learnModel(r.getMaxUid(),r.getMaxIid(),0.01,0.01,0.01,0.01,trainingDict,350, 15,
					r.numberOfTransactions)

np.savez_compressed("modelFile",W=W,H=H)
modelf=np.load("modelFile.npz")
W=modelf['W']
H=modelf['H']
modelf.close()

rec=test.svdtest(W,H,trainingDict)

print test.hitrate(testDict,rec.getRec,10)
