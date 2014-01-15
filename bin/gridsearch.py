import numpy as np
import recommender.BPRMF
import util.reader
import sys
import wsdm
import time 
import cPickle

filename = sys.argv[1]
i = float(sys.argv[2])
numberOfFactors = 16
epochs = 15

parameters = [0.0001,0.001,0.01,0.1]

#R = wsdm.loadR(filename)
r = util.reader.fastStringSepReader(filename,"\t")
#output = open("justfordebugging.npz", "wb")
#cPickle.dump(r, output, -1)

R = r.getR()

numberOfUsers = r.getMaxUid()
numberOfItems = r.getMaxIid()
numberOfTransactions = r.numberOfTransactions
filename = filename.split("/")[-1]

for d in parameters: # reg
    print("Training with lrate: %f and reg: %f" %(i,d))
    W, H = recommender.BPRMF.learnModel(numberOfUsers,
                                numberOfItems,
                                d, d, d,
                                i,
                                R,
                                numberOfFactors,
                                epochs,
                                numberOfTransactions)
    np.savez_compressed(
       filename + "_" + 
       str(i) + "_" +
       str(d) + "_" +
       str(time.time()) +
       ".npz" , W=W, H=H)
