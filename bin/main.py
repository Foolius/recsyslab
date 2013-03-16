import evaluation
import reader
import baselines
import test
import helper
import bpr
import numpy as np

r=reader.tabSepReader("../kleinu.data")

#trainingDict,testDict=evaluation.split(r.getR())

#helper.writeInternalToFile(r,trainingDict,"training")
#helper.writeInternalToFile(r,testDict,"test")

#rec=baselines.constant(trainingDict)
#print test.hitrate(testDict, rec.getRec,10)

bpr.foo(9,r)
