class idOrigDict(object):

    def __init__(self):
        self.orig2id = {}
        self.id2orig = {}
        self.id = 0

    def add(self, orig):
        if not orig in self.orig2id.keys():
            self.orig2id[orig] = self.id
            self.id2orig[self.id] = orig
            self.id += 1
        return self.getId(orig)

    def getOrig(self, id):
        return self.id2orig[id]

    def getId(self, orig):
        return self.orig2id[orig]

import functools


class Namespace():
    pass


def cache(fn):
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
    f = file(filename, "w")
    for r in toSave.iterkeys():
        ri = reader.getOriginalUid(r)
        for i in toSave[r]:
            ii = reader.getOriginalIid(i)
            f.write("%r\t%r\n" % (ri, ii))
    f.close()


def writeInternalToFile(reader, toSave, filename):
    f = file(filename, "w")
    for r in toSave.iterkeys():
        for i in toSave[r]:
            f.write("%r\t%r\n" % (r, i))
    f.close()


def sortList(scorelist):
    """Gets a list of tuples (itemid,score),
    sorts by score decreasing."""
    sortedscorelist = sorted(scorelist,
                             key=lambda(k, v): v,
                             reverse=True)
    return sortedscorelist


def listToSet(sortedscorelist, n):
    """Gets a list like sortList returns
    and returns a set with the first n
    items, or less, when there are not
    enough items"""
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

# sortResults("RankMFXresults.data")


def printMatrix(m):
    for i in xrange(0, m.shape[0]):
        s = ""
        for j in xrange(0, m.shape[1]):
            s += "%r\t" % m[i, j]
        print s
