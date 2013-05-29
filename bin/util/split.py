"""Methods to split a database with the leave-one-out method.

   split        --  splits a reader into two new dicts
   splitMatrix  --  splits a matrix into a matrix and a dict
   """
import random
import copy


def split(R, seed):
    """Splits a database into two dicts.

    Splits after the leave-one-out method which means for every user in the
    database it takes one item out of the database and into a new one.
    The first returned dict is the database with one item missing for each
    user. The second returned dict has the missing items.

    R is a dict of the database.
    seed is a seed for the randomness.
    """

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
    """Splits a matrix into two new dicts.

    Returns an User x Item Matrix with one entry of each user set to 0
    and a User -> Item Dict with the missing entrys.

    M is an User x Item Matrix.
    seed is a seed for the randomness.
    """
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
        temp = bigSplit[user, item]
        bigSplit[user, item] = 0
        smallSplitDict[user] = list([(item, temp)])

    return bigSplit, smallSplitDict
