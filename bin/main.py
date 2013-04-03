import split
import reader
import baselines
import test
import helper
import bprmf
import numpy as np
import RankMFX
import cPickle
import time
import datetime

SEED1=1
SEED2=11
EPOCHS=15
features=350

#learningratevalues=[0.001,0.01,0.1]
#regularizationvalues=[0,0.001,0.01,0.1,1]
learningratevalues=[0.1]
regularizationvalues=[0.01]

def readDBandSplit(dbfile):
    r=reader.tabSepReader(dbfile)
    fulltrain,testDict=split.split(
        r.getR(),SEED1)
    trainingDict,evalDict=split.split(
        fulltrain,SEED2)
    output=open("splits.npz","wb")
    cPickle.dump(r,output,-1)
    cPickle.dump(trainingDict,output,-1)
    cPickle.dump(fulltrain,output,-1)
    cPickle.dump(testDict,output,-1)
    cPickle.dump(evalDict,output,-1)
    output.close()
    return r,trainingDict,fulltrain,testDict,evalDict

#r,trainingDict,fulltrain,testDict,evalDict=readDBandSplit("u.data")

def loadData():
    inputfile=open("splits.npz","rb")
    r=cPickle.load(inputfile)
    trainingDict=cPickle.load(inputfile)
    fulltrain=cPickle.load(inputfile)
    testDict=cPickle.load(inputfile)
    evalDict=cPickle.load(inputfile)
    inputfile.close()
    return r,trainingDict,fulltrain,testDict,evalDict

#r,trainingDict,fulltrain,testDict,evalDict=loadData()

#helper.writeInternalToFile(
    #r,trainingDict,"training")
#helper.writeInternalToFile(
    #r,testDict,"test")

def constant(r,trainingDict,testDict):
    rec=baselines.constant(trainingDict)
    print("Hitrate for constant: %r"
        %test.hitrate(
            testDict,rec.getRec,10))

#constant(r,trainingDict,testDict)

def random(r,trainingDict,testDict):
    rec=baselines.randomRec(trainingDict)
    print("Hitrate for random: %r"
        %test.hitrate(
            testDict,rec.getRec,10))

#random(r,trainingDict,testDict)

def learnRankMFX(r,trainingDict,reg,ler):
    rank=RankMFX.RankMFX()
    W,H = rank.learnModel(
        r.getMaxUid(),r.getMaxIid(),
        reg,reg,reg,ler,trainingDict,
        features,EPOCHS,
        r.numberOfTransactions)
    np.savez_compressed(
        "RankMFXModelFile",W=W,H=H)
    return W,H

#W,H=learnRankMFX(r,trainingDict,0.1,0.1)

def learnBPRMF(r,trainingDict,reg,ler):
    W,H = bprmf.learnModel(
        r.getMaxUid(),r.getMaxIid(),
        reg,reg,reg,ler,trainingDict,
        features,EPOCHS,
        r.numberOfTransactions)
    np.savez_compressed(
        "BPRMFModelFile",W=W,H=H)
    return W,H

#learnBPRMF(r,trainingDict)

def loadM(name):
    modelf=np.load(name+".npz")
    W=modelf['W']
    H=modelf['H']
    modelf.close
    return W,H

#W,H=loadM("RankMFXModelFile")
#W,H=loadM("BPRMFModelFile")

def testMF(W,H,trainingDict,testDict):
    t=test.MFtest(W,H,trainingDict)
    hr=test.hitrate(testDict,t.getRec,10)
    return hr

#testMF(W,H,trainingDict,testDict)

ts=time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
file=open("results.data","a")
file.write("Started at: "+st+"\n")
print("Started at: "+st+"\n")

def tweak(learnModel,r,trainingDict,fulltrain,testDict,evalDict):
    legend="Algorithm|Regconstant|Learningrate|Epochs|Features|Hitrate\n"
    file.write(legend)

    trainingDict=fulltrain
    evalDict=testDict

    results=[]

    for reg in regularizationvalues:
        for ler in learningratevalues:
            W,H=learnModel(
                r,trainingDict,reg,ler)
            results.append(
                testMF(W,H,trainingDict,
                evalDict))
            s=(learnModel.__name__+"|%r|%r|%r|%r|%r\n"
                %(reg,ler,EPOCHS,features,
                results[-1]))
            print("")
            print(legend+s)
            file.write(s)
    return results[-1]

    index=results.index(max(results))
    count=-1
    for reg in regularizationvalues:
        for ler in learningratevalues:
            print("%r %r %r"%(count,reg,ler))
            count+=1
            if count!=index:
                continue
            W,H=learnModel(
                r,fulltrain,reg,ler)
            hr=testMF(W,H,fulltrain,
                testDict)
            s=("Best:\n"+learnModel.__name__+"|%r|%r|%r|%r\n\n"
                %(reg,ler,EPOCHS,
                hr))
            print("")
            print(legend+s)
            file.write(s)


##r,trainingDict,fulltrain,testDict,evalDict=readDBandSplit("u.data")


def tweak10times():
    for i in xrange(0,10):
        print("BPRMF %r"%i)
        tweak(learnBPRMF,r,trainingDict,fulltrain,testDict,evalDict)

    for i in xrange(0,10):
        print("RankMFX%r"%i)
        tweak(learnRankMFX,r,trainingDict,fulltrain,testDict,evalDict)

def findBestFeature():
    features=512
    ult=0.0
    penult=0.0
    dir=True
    while(True):
        penult=ult
        ult=tweak(learnBPRMF,r,trainingDict,fulltrain,testDict,evalDict)
        #ult=tweak(learnRankMFX,r,trainingDict,fulltrain,testDict,evalDict)
        if ult>penult and dir:
            features+=features/2
        if ult>penult and not dir:
            features-=features/2
            
r=reader.tabSepReader("kleinu.data")
rf=open("reader.npz","wb")
cPickle.dump(r,rf,-1)
#print r.getMatrix()
rf.close()

import knn
k=knn.knn(r.getMatrix())
#kf=open("knn.npz","wb")
#cPickle.dump(k,kf,-1)
#kf.close()
#kf=open("knn.npz","rb")
#k=cPickle.load(kf)
print r.getMatrix()
print k.sim
k.getRec(1,10)

file.close
