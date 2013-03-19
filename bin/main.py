import split
import reader
import baselines
import test
import helper
import bprmf
import numpy as np
import RankMFX
import cPickle

def readDBandSplit(dbfile):
	r=reader.tabSepReader(dbfile)
#	print(len(r.getR()[4]))
	trainingDict,testDict=split.split(r.getR())
#	print(len(r.getR()[4]))
	output=open("testDict.npz","wb")
	cPickle.dump(r,output,-1)
	cPickle.dump(trainingDict,output,-1)
	cPickle.dump(testDict,output,-1)
	output.close()
	return r,trainingDict,testDict

r,trainingDict,testDict=readDBandSplit("u.data")

def loadData():
	inputfile=open("testDict.npz","rb")
	r=cPickle.load(inputfile)
	trainingDict=cPickle.load(inputfile)
	testDict=cPickle.load(inputfile)
	inputfile.close()
	return r,trainingDict,testDict

r,trainingDict,testDict=loadData()

#helper.writeInternalToFile(r,trainingDict,"training")
#helper.writeInternalToFile(r,testDict,"test")

def constant(r,trainingDict,testDict):
	rec=baselines.constant(trainingDict)
	print("Hitrate for constant: %r"% test.hitrate(testDict, rec.getRec,10))

#constant(r,trainingDict,testDict)

def random(r,trainingDict,testDict):
	rec=baselines.randomRec(trainingDict)
	print("Hitrate for random: %r" %test.hitrate(testDict,rec.getRec,10))

#random(r,trainingDict,testDict)

def learnRankMFX(r,trainingDict):
	rank=RankMFX.RankMFX()
	W,H = rank.learnModel(r.getMaxUid(),r.getMaxIid(),0.01,0.01,0.01,0.01,trainingDict,350,5,
							r.numberOfTransactions)
	np.savez_compressed("RankMFXModelFile",W=W,H=H)

#learnRankMFX(r,trainingDict)

def learnBPRMF(r,trainingDict):
	W,H = bprmf.learnModel(r.getMaxUid(),r.getMaxIid(),0.01,0.01,0.01,0.01,trainingDict,350, 9,
						r.numberOfTransactions)
	np.savez_compressed("BPRMFModelFile",W=W,H=H)

learnBPRMF(r,trainingDict)

def loadM(name):
	modelf=np.load(name+".npz")
	W=modelf['W']
	H=modelf['H']
	modelf.close
	return W,H

#W,H=loadM("RankMFXModelFile")
W,H=loadM("BPRMFModelFile")

def testMF(W,H,trainingDict,testDict):
	t=test.MFtest(W,H,trainingDict)
	print ("Hitrate for MF: %r" %test.hitrate(testDict,t.getRec,10))

testMF(W,H,trainingDict,testDict)
