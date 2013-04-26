import numpy as np


def getScoreMF(origUid, origIid, W, H, r):
    """Returns the score of one item for one user.
    Itemid and Userid are the original IDs."""
    uid = r.uidDict.getId(origUid)
    iid = r.iidDict.getId(origIid)

    return np.dot(W[uid], H[iid])


def getExternalRec(getRec, r):
    """ Returns a function with returns
    the n best recommendations from getRec.
    The recommendations are with the original IDs"""

    def wrapper(extUid, n):
        uid = r.uidDict.getId(extUid)

        recs = getRec(uid, n)

        extRecs = []
        for i in recs:
            extRecs.append(r.iidDict.getOrig(i))

        return extRecs

    return wrapper
