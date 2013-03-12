import evaluation
import reader
import baselines
import test
import helper

r=reader.tabSepReader("../u.data")
trainingDict,testDict=evaluation.split(r.getR())

trainingFile=file("training","w")
for t in trainingDict.iterkeys():
	ti=r.getOriginalUid(t)
	for i in trainingDict[t]:
		#i=r.getOriginalIid(i)
		trainingFile.write("%r\t%r\n"%(t,i))
trainingFile.close()

testFile=file("test","w")
for t in testDict.iterkeys():
	ti=r.getOriginalUid(t)
	i=r.getOriginalIid(testDict[t])
	testFile.write("%r\t%r\n"%(ti,i))
testFile.close()

rec=baselines.constant(trainingDict)
print test.hitrate(testDict, rec.getRec,10)
