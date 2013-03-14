import evaluation
import reader
import baselines
import test
import helper
import bpr

r=reader.tabSepReader("../kleinu.data")
for d in bpr.computeDs(r):
	print d


#trainingDict,testDict=evaluation.split(r.getR())

#helper.writeInternalToFile(r,trainingDict,"training")
#helper.writeInternalToFile(r,testDict,"test")

#rec=baselines.constant(trainingDict)
#print test.hitrate(testDict, rec.getRec,10)
