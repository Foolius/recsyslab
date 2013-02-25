import evaluation
import reader
import baselines
import test

r=reader.tabSepReader("../u.data")


train,eval,testSet=evaluation.split(r.getSimpleList(),3,2,2)

const=baselines.constant(r.getR())
#testSet=[[1,1]]
print test.hitrate(testSet,const.getRec,10)
