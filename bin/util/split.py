import random
import copy


def split(R, seed):

    random.seed(seed)
    split = {}
    training = {}

    count = 0
    for user in R.iterkeys():
        if count % 100 == 0:
            print("%r Users split." % count)
        count += 1

        item = random.sample(R[user], 1)[0]
        # because random.sample gives a list
        split[user] = set([item])
        s = copy.deepcopy(R[user])
        s.discard(item)
        training[user] = s
    return training, split


def splitMatrix(M, seed):
    """Takes an User x Item Matrix and returns
    an User x Item Matrix with one item per user missing
    and a User -> Item Dict with the missing entrys."""
    random.seed(seed)
    bigSplit = M.copy(order='A')
    smallSplitDict = {}

    count = 0
    for user in xrange(0, bigSplit.shape[0]):
        if count % 100 == 0:
            print("%r Users split." % count)
        count += 1

        item = random.randint(0, bigSplit.shape[1] - 1)
        while bigSplit[user, item] == 0:
            item = random.randint(0, bigSplit.shape[1] - 1)
        bigSplit[user, item] = 0
        smallSplitDict[user] = set([(item, 0)])

    return bigSplit, smallSplitDict
