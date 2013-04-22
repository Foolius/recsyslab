import split
import reader
import baselines
import test
import numpy as np
import cPickle
import time
import datetime
import mf

SEED1 = 1213451205
SEED2 = 10989084
EPOCHS = 10
features = 150

# learningratevalues=[0.001,0.01,0.1]
# regularizationvalues=[0,0.001,0.01,0.1,1]
learningratevalues = [0.1]
regularizationvalues = [0.01]


def readDBandSplit(dbfile):
    r = reader.tabSepReader(dbfile)
    fulltrain, testDict = split.split(
        r.getR(), SEED1)
    trainingDict, evalDict = split.split(
        fulltrain, SEED2)
    output = open("splits.npz", "wb")
    cPickle.dump(r, output, -1)
    cPickle.dump(trainingDict, output, -1)
    cPickle.dump(fulltrain, output, -1)
    cPickle.dump(testDict, output, -1)
    cPickle.dump(evalDict, output, -1)
    output.close()
    return r, trainingDict, fulltrain, testDict, evalDict

r, trainingDict, fulltrain, testDict, evalDict = readDBandSplit("u.data")


def loadData():
    inputfile = open("splits.npz", "rb")
    r = cPickle.load(inputfile)
    trainingDict = cPickle.load(inputfile)
    fulltrain = cPickle.load(inputfile)
    testDict = cPickle.load(inputfile)
    evalDict = cPickle.load(inputfile)
    inputfile.close()
    return r, trainingDict, fulltrain, testDict, evalDict

#r, trainingDict, fulltrain, testDict, evalDict = loadData()

# helper.writeInternalToFile(
    # r,trainingDict,"training")
# helper.writeInternalToFile(
    # r,testDict,"test")


def constant(r, trainingDict, testDict):
    rec = baselines.constant(trainingDict)
    print("Hitratefor constant: %r" %
          test.hitrate(testDict, rec.getRec, 10))

# constant(r, trainingDict, testDict)


def random(r, trainingDict, testDict):
    rec = baselines.randomRec(trainingDict)
    print("AUC for random: %r" % test.auc(testDict, rec.getRec, r))

# random(r, trainingDict, testDict)


def testMF(W, H, trainingDict, testDict, n):
    t = test.MFtest(W, H, trainingDict)
    test.hitrate(testDict, t.getRec, n)
#    test.f1(testDict, t.getRec, n)
#    test.precision(testDict, t.getRec, n)
#    test.mrhr(testDict, t.getRec, n)
#    hr = test.auc(testDict, t.getRec, r)
#    return hr


def learnMF(r, trainingDict, reg, ler, lossF, dlossF):
    W, H = mf.learnModel(
        r.getMaxUid(), r.getMaxIid(),
        reg, reg, reg, ler, trainingDict,
        features, EPOCHS,
        r.numberOfTransactions,
        lossF, dlossF)
#    np.savez_compressed(
#        "BPRMFModelFile", W=W, H=H)
    return W, H

# RankMFX
#W, H = learnMF(r, trainingDict, 0.01, 0.1, mf.hingeLoss, mf.dHingeLoss)
#testMF(W, H, trainingDict, testDict, 10)

# BPRMF
#W, H = learnMF(r, trainingDict, 0.01, 0.1, mf.logLoss, mf.dLogLoss)
#testMF(W, H, trainingDict, testDict, 10)


def loadM(name):
    modelf = np.load(name + ".npz")
    W = modelf['W']
    H = modelf['H']
    modelf.close
    return W, H

# W,H=loadM("RankMFXModelFile")
# W, H = loadM("BPRMFModelFile")


ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

file = open("results.data", "a")
file.write("Started at: " + st + "\n")
print("Started at: " + st + "\n")
