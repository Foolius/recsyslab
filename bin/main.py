import evaluation
import reader
import baselines
import test
import helper

r=reader.tabSepReader("../u.data")
#training,test=evaluation.split(r.getR())
training=r.getR()
test={}
trainingFile=file("training","w")
for t in training.iterkeys():
	ti=r.getOriginalUid(t)
	for i in training[t]:
		#i=r.getOriginalIid(i)
		trainingFile.write("%r\t%r\n"%(t,i))
trainingFile.close()

testFile=file("test","w")
for t in test.iterkeys():
	ti=r.getOriginalUid(t)
	i=r.getOriginalIid(test[t])
	testFile.write("%r\t%r\n"%(ti,i))
testFile.close()
print("origuid(242):%r")%r.getOriginalUid(242)
print("origiid(242):%r")%r.getOriginalIid(242)
