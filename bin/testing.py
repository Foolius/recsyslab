def mf():
    import reader
    r = reader.tabSepReader("u.data")

    import split
    train, test1 = split.split(r.getR(), 1234567890)

    import mf
    # W, H = mf.learnModel(r.getMaxUid(), r.getMaxIid(), 0.01, 0.01, 0.01,
    #                     0.1, train, 150, 3, r.numberOfTransactions,
    #                     mf.logLoss, mf.dLogLoss)
    import numpy as np
    # np.savez_compressed(
    #    "BPRMFModelFile", W=W, H=H)
    modelf = np.load("BPRMFModelFile" + ".npz")
    W = modelf['W']
    H = modelf['H']
    modelf.close

    import test
    t = test.MFtest(W, H, train)
    # test.hitrate(test1, t.getRec, 10)
    scoredict = t.getRec(201, 10)
    for i in scoredict.keys():
        print i, scoredict[i], test.getScoreMF(r.uidDict.getOrig(201),
                                               r.iidDict.getOrig(i), W, H, r)
    print len(scoredict)

mf()


def knn():
    import reader
    r = reader.tabSepReader("u.data")

    import split
    train, test1 = split.splitMatrix(r.getMatrix(), 1234567890)

    import knn
    k = knn.itemKnn(train, 10)

    import cPickle
    # output = open("knn.npz", "wb")
    # cPickle.dump(k, output, -1)
    # output.close()
    inputfile = open("knn.npz", "rb")
    k = cPickle.load(inputfile)
    inputfile.close()

    import test
    test.hitrate(test1, k.getRec, 10)


def simple():
    import reader
    r = reader.tabSepReader("u.data")

    import split
    train, test1 = split.split(r.getR(), 1234567890)

    import baselines
    c = baselines.randomRec(r.getR())

    import test
    test.hitrate(test1, c.getRec, 10)
