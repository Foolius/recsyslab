"""Several helper functions and a helper class."""


class idOrigDict(object):
    """Class two map external/original IDs to internal IDs and vice versa."""

    def __init__(self):
        """Initialization."""
        self.orig2id = {}
        self.id2orig = {}
        self.id = 0

    def add(self, orig):
        """Add a new original ID.

        Returns the internal ID the passed original ID got mapped to.
        If the passed ID is already mapped nothing happens except the
        mapped internal ID is returned."""
        if not orig in self.orig2id.keys():
            self.orig2id[orig] = self.id
            self.id2orig[self.id] = orig
            self.id += 1
        return self.getId(orig)

    def getOrig(self, id):
        """Returns the original ID which is mapped to the passed internal ID.
        """
        return self.id2orig[id]

    def getId(self, orig):
        """Returns the internal ID which is mapped to the passed orinigal ID.
        """
        return self.orig2id[orig]


def normRowNorm(m):
    """Normalize the matrix in place so each row of the matrix has norm 1."""
    import numpy as np
    for i in xrange(0, m.shape[0]):
        m[i] /= np.linalg.norm(m[0])
    return m


def normRowSum(m):
    """Normalize the matrix in place so each column of the matrix has norm 1.
    """
    import numpy as np
    for i in xrange(0, m.shape[0]):
        m[i] /= np.sum(m[0])
    return m


def cache(fn):
    """Decorator to cache the result of the function fn."""
    import functools

    class Namespace():
        pass
    ns = Namespace()
    ns.fail = 0
    ns.success = 0
    ns.count = 0
    cacheDict = {}

    @functools.wraps(fn)
    def cached(*args):
        if (ns.count % 100000 == 0):
            print("Success: %r Fail: %r Sum: %r Count: %r"
                  % (ns.success, ns.fail, (ns.success + ns.fail), ns.count))
        ns.count += 1
        try:
            result = cacheDict[args]
            ns.success += 1
            return result
        except KeyError:
            ns.fail += 1
            result = cacheDict[args] = fn(*args)
            return result

    return cached


def writeOrigToFile(reader, toSave, filename):
    """Writes a database into a file with the original IDs.

        reader  --  reader object
        toSave  --  Part of the database to write
        filename--  Name of the file

    Writes toSave into a file with the name filename but first the
    internal IDs in toSave get mapped to the original IDs.
    """
    f = file(filename, "w")
    for r in toSave.iterkeys():
        ri = reader.getOriginalUid(r)
        for i, rating in toSave[r]:
            ii = reader.getOriginalIid(i)
            f.write("%r\t%r\t%r\n" % (ri, ii, rating))
    f.close()


def writeInternalToFile(reader, toSave, filename):
    """Writes a database into a file with the internal IDs.

        reader  --  reader object
        toSave  --  Part of the database to write
        filename--  Name of the file

    Writes toSave into a file with the name filename.
    """

    f = file(filename, "w")
    for r in toSave.iterkeys():
        for i, rating in toSave[r]:
            f.write("%r\t%r\t%r\n" % (r, i, rating))
    f.close()


def sortList(scorelist):
    """Gets a list of tuples (itemid, score), sorts by score decreasing."""
    sortedscorelist = sorted(scorelist,
                             key=lambda(k, v): v,
                             reverse=True)

    l = []
    for i in sortedscorelist:
        l.append(i[0])
    return l


def listToSet(sortedscorelist, n):
    """Converts a list into a set with size n.

    Gets a list like sortList returns and returns a set with the first n
    items, or less, when there are not enough items"""
    if len(sortedscorelist) < n:
        n = len(sortedscorelist)
    s = set()
    for i in sortedscorelist[:n]:
        s.add(i[0])
    return s


def sortResults(name):
    infile = open(name, 'r')
    outfile = open("out" + name, 'w')
    b = True
    l = []
    for line in infile:
        if line[0] == "S":
            outfile.write(line)
            continue
        if line[0] == "A":
            if b:
                outfile.write(line)
            b = False
            continue
        l.append(line.strip().split("|", -1))
    l = sorted(l, key=lambda(a, b, c, d, e): e, reverse=True)

    for e in l:
        outfile.write("|".join(e))
        outfile.write("\n")
        print("|".join(e))

        # outfile.write(e)

    outfile.close()
    infile.close()


def printMatrix(m):
    """Prints a whole matrix.

    Prints the whole matrix m without replacing stuff with dots
    like it normally does when the matrix is to large."""
    for i in xrange(0, m.shape[0]):
        s = ""
        for j in xrange(0, m.shape[1]):
            s += "%r\t" % m[i, j]
        print s


def randDataset(user, items, p, seed, filename):
    """Generates a random dataset and writes it into a file.

        user    --  number of users
        items   --  number of items
        p       --  percentage of ones in the dataset
        seed    --  seed for the randomness
        """
    import random
    random.seed(seed)
    f = open(filename, 'w')

    for i in xrange(0, user):
        for j in xrange(0, items):
            if(random.randint(0, 100) < p):
                f.write("%r\t%r\n" % (i, j))
    f.close


def dictToMatrix(d):
    """Converts a dict like reader.getR() returns to a matrix."""
    import numpy as np
    rows = max(d)
    lines = 0
    for data in d.iteritems():
        for item, rating in iter(data[1]):
            if item > lines:
                lines = item

    m = np.matrix(np.zeros((rows + 1, lines + 1)))

    for data in d.iteritems():
        for item, rating in iter(data[1]):
            m[data[0], item] = rating

    return m


def getScoreMF(origUid, origIid, W, H, r):
    """Returns the score of one item for one user with an MF model.
        origUid --  original User ID
        origIid --  original Item ID
        W, H    --  The MF model like returned by recommender.mf for example
        r       --  a reader object with the database
    """
    uid = r.uidDict.getId(origUid)
    iid = r.iidDict.getId(origIid)

    import numpy as np

    return np.dot(W[uid], H[iid])


def getExternalRec(getRec, r):
    """Converts getRec so it takes and returns only the original IDs.

        r   --  reader object"""
    def wrapper(extUid, n):
        uid = r.uidDict.getId(extUid)

        recs = getRec(uid, n)

        extRecs = []
        for i in recs:
            extRecs.append(r.iidDict.getOrig(i))

        return extRecs

    return wrapper
