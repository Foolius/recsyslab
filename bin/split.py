import random
import copy
import numpy as np

def split(R,seed):

    random.seed(seed)
    split={}
    training={}

    for user in R.iterkeys():
        item=random.sample(R[user],1)[0] #because random.sample gives a list
        split[user]=set([item])
        s=copy.deepcopy(R[user])
        s.discard(item)
        training[user]=s
    return training,split

def splitMatrix(M,seed):
    """Takes an User x Item Matrix and returns
    an User x Item Matrix with one item per user missing
    and a User x Item Matrix with the missing entrys."""
    random.seed(seed)
    bigSplit=M.copy(order='A')
    smallSplitDict={}
    #smallSplit=np.matrix(np.zeros(M.shape))

    count=0
    for user in xrange(0,bigSplit.shape[0]):
        if count%100==0:
            #print("%r Users split."%count)
        count+=1

        item=random.randint(0,bigSplit.shape[1]-1)
        while bigSplit[user,item]==1:
            item=random.randint(0,bigSplit.shape[1]-1)
        bigSplit[user,item]=0
        smallSplitDict[user]=set([item])
        #smallSplit[u,item]=1

    return bigSplit,smallSplitDict
