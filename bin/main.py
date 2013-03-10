import evaluation
import reader
import baselines
import test
import helper

h=helper.idOrigDict()
h.add(1)
h.getOrig(0)


def foo():
	r=reader.tabSepReader("../kleinu.data")
	training,test=evaluation.split(r.getR())

	trainingFile=file("training","w")
	for t in training.iterkeys():
		for i in training[t]:
			print(training)
			t=r.getOriginalUid(t)
			i=r.getOriginalIid(i)
			trainingFile.write("%r\t%r\n"%(t,i))
	trainingFile.close()

	testFile=file("test","w")
	for t in test.iterkeys():
		testFile.write("%r\t%r\n"%(t,test[t]))
	testFile.close()

foo()
