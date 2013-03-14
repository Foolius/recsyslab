import evaluation
import reader
import baselines
import test
import helper

r=reader.tabSepReader("../u.data")
trainingDict,testDict=evaluation.split(r.getR())

helper.writeToFile(r,trainingDict,"training")
helper.writeToFile(r,testDict,"test")

rec=baselines.constant(trainingDict)
print test.hitrate(testDict, rec.getRec,10)
