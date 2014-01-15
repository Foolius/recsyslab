def slopeone():
    from util import reader
    r = reader.tabSepReader("u.data")

    from util import split
    train, test1 = split.split(r.getR(), 12320894329854567890)

    from recommender import slopeone
    so = slopeone.slopeone(train)

    # import cPickle
    # output = open("slopeone.npz", "wb")
    # cPickle.dump(so, output, -1)
    # output.close()

    # inputfile = open("slopeone.npz", "rb")
    # so = cPickle.load(inputfile)
    # inputfile.close()

    from util import test
    test.auc(test1, so.getRec, r)

# slopeone()


def svd():
    from util import reader
    r = reader.tabSepReader("u.data")

    from util import split
    train, test1 = split.split(r.getR(), 1234567890)

    from recommender import svd
    W, H = svd.learnModel(r.getMaxUid(), r.getMaxIid(),
                          0.0002, train, 1000, 25, r.numberOfTransactions)
    import numpy as np
    np.savez_compressed(
        "SVDModelFile", W=W, H=H)
    # modelf = np.load("BPRMFModelFile" + ".npz")
    # W = modelf['W']
    # H = modelf['H']
    # modelf.close

    from util import test
    t = test.MFtest(W, H, train)
    test.hitrate(test1, t.getRec, 10)

# svd()


def mf():
    from util import reader
    r = reader.fastStringSepReader("u.data", "\t")

    from util import split
    train, test1 = split.split(r.getR(), 1234567890)

    from recommender import BPRMF
    W, H = BPRMF.learnModel(r.getMaxUid(), r.getMaxIid(), 0.01, 0.01, 0.01,
                         0.1, train, 150, 3, r.numberOfTransactions)
    import numpy as np
    # np.savez_compressed(
    #    "BPRMFModelFile", W=W, H=H)
    # modelf = np.load("BPRMFModelFile" + ".npz")
    # W = modelf['W']
    # H = modelf['H']
    # modelf.close

    from recommender import mf
    from util import test
    t = mf.MFrec(W, H, train)
    test.hitrate(test1, t.getRec, 10)

#mf()

def fastBPRMF():
    from util import reader
    r = reader.fastStringSepReader("u.data", "\t")

    from util import split
    train, test1 = split.split(r.getR(), 1234567890)

    from recommender import fastBPRMF
    W, H = fastBPRMF.learnModel(r.getMaxUid(), r.getMaxIid(), 0.01, 0.01, 0.01,
                         0.1, train, 150, 3)
    import numpy as np
    # np.savez_compressed(
    #    "BPRMFModelFile", W=W, H=H)
    # modelf = np.load("BPRMFModelFile" + ".npz")
    # W = modelf['W']
    # H = modelf['H']
    # modelf.close

    from recommender import mf
    from util import test
    t = mf.MFrec(W, H, train)
    test.hitrate(test1, t.getRec, 10)

#fastBPRMF()


def knn():
    from util import reader
    r = reader.stringSepReader("u.data", "\t")

    from util import split
    train, test1 = split.splitMatrix(r.getMatrix(), 1234567890)

    from recommender import knn
    k = knn.userKnn(train, 10)

    from util import test
    print test.hitrate(test1, k.getRec, 10)

    import cPickle
    output = open("knn.npz", "wb")
    cPickle.dump(k, output, -1)
    output.close()

    # inputfile = open("knn.npz", "rb")
    # so = cPickle.load(inputfile)
    # inputfile.close()

# knn()


def simple():
    from util import reader
    r = reader.stringSepReader("u.data", "\t")

    from util import split
    train, test1 = split.split(r.getR(), 1234567890)

    from recommender import nonpersonalized
    c = nonpersonalized.randomRec(r.getR(), 3284092)

    from util import test
    test.auc(test1, c.getRec, r)

#simple()
