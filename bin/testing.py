def svd():
    import reader
    r = reader.tabSepReader("u.data")

    import split
    train, test1 = split.split(r.getR(), 1234567890)

    import svd
    W, H = svd.learnModel(r.getMaxUid(), r.getMaxIid(),
                          0.0002, train, 1000, 25, r.numberOfTransactions)
    import numpy as np
    np.savez_compressed(
        "SVDModelFile", W=W, H=H)
    # modelf = np.load("BPRMFModelFile" + ".npz")
    # W = modelf['W']
    # H = modelf['H']
    # modelf.close

    import test
    t = test.MFtest(W, H, train)
    test.hitrate(test1, t.getRec, 10)

svd()


def mf():
    import reader
    r = reader.tabSepReader("u.data")

    import split
    train, test1 = split.split(r.getR(), 1234567890)

    import mf
    W, H = mf.learnModel(r.getMaxUid(), r.getMaxIid(), 0.01, 0.01, 0.01,
                         0.1, train, 150, 3, r.numberOfTransactions,
                         mf.logLoss, mf.dLogLoss)
    import numpy as np
    # np.savez_compressed(
    #    "BPRMFModelFile", W=W, H=H)
    # modelf = np.load("BPRMFModelFile" + ".npz")
    # W = modelf['W']
    # H = modelf['H']
    # modelf.close

    import test
    t = test.MFtest(W, H, train)
    test.hitrate(test1, t.getRec, 10)

# mf()


def knn():
    import reader
    r = reader.tabSepReader("u.data")

    import split
    train, test1 = split.splitMatrix(r.getMatrix(), 1234567890)

    import knn
    k = knn.itemKnn(train, 10)

    import test
    print test.f1(test1, k.getRec, 10)

# knn()


def simple():
    import reader
    r = reader.tabSepReader("u.data")

    import split
    train, test1 = split.split(r.getR(), 1234567890)

    import primitive
    c = primitive.randomRec(r.getR())

    import test
    test.auc(test1, c.getRec, r)
