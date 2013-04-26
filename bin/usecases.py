# Reading a database file
import reader
r = reader.tabSepReader("u.data")

# Get 10 recommendations with simple algorithms
# for userid 201.
import primitive
import external
rand = primitive.randomRec(r.getR())
getRec = external.getExternalRec(rand.getRec, r)
print getRec(97, 10)

# Train a MF model.
import mf

reg = 0.01  # Regularization constant
ler = 0.1  # Learning rate
features = 150  # number of features
EPOCHS = 3  # number of epochs

W, H = mf.learnModel(
    r.getMaxUid(), r.getMaxIid(),
    reg, reg, reg, ler, r.getR(),
    features, EPOCHS,
    r.numberOfTransactions,
    mf.logLoss, mf.dLogLoss)  # With logLoss it will be BPRMF

# Get recommendations with a MF model.
import test
import external
t = test.MFtest(W, H, r.getR())
getRec = external.getExternalRec(t.getRec, r)
print getRec(97, 10)

# Calculate the hitrate of item based cosine KNN.
import split
splittedMatrix, testDict = split.splitMatrix(r.getMatrix(), 1234567890)

import knn
neighbors = 30  # number of neighbors
k = knn.itemKnn(splittedMatrix, neighbors)

import test
print test.hitrate(testDict, k.getRec, 10)
