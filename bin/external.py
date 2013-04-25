

def getScoreMF(origUid, origIid, W, H, r):
    """Returns the score of one item for one user.
    Itemid and Userid are the original IDs."""
    uid = r.uidDict.getId(origUid)
    iid = r.iidDict.getId(origIid)

    return np.dot(W[uid], H[iid])


def getRec(
