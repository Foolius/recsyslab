"""Module with several metrics to test the recommender algorithms.

    hitrate     --  Returns #hits, #items
    precision   --  Returns #hits / n
    f1          --  Returns the result of a F1 test
    mrhr        --  Returns the Mean Reciprocal Hitrate
    auc         --  Returns the Area under the curve
    MFtest      --  Returns a recommender function built from a MF model"""


def hitrate(testR, recommender, n):
    """Returns the number of hits and the number of items it was tested with.

    testR is a dict with an internal UserID as a dict and a list of items as
    values. Normally testR is the second dict split.split returns.
    The list can have a lenght greater than 1.

    recommender is a function which takes an internal UserID and n and returns
    n items recommender for the UserID.

    n is the number of items the recommender can recommend.

    hits = number of items from testR the recommender guessed right.
    items = the number of items in testR.

    hits, items and hits / items will be printed.
    hits, items will get returned.

    hits / items gives the hitrate or recall.

    See also: "Application of Dimensionality Reduction in Recommender System
    -- A Case Study" by Badrul M. sarcar et al.
    """
    hits = 0.0
    items = 0.0
    for u in testR.iterkeys():
        if u % 100 == 0:
            print("%r users tested" % u)
            print("Hits so far: %r" % hits)
        recs = recommender(u, n)
        if len(recs) != n and not n == -1:
            print("Fatal error: not the right number of items.")
        testSet = set()
        for t in testR[u]:
            testSet.add(t[0])
        hits += len(testSet.intersection(set(recs)))
        items += len(testSet)

    print("Number of hits: %r" % hits)
    print("Number of possible hits: %r" % items)
    print("Hitrate: %r" % (hits / items))
    return hits, items


def precision(testR, recommender, n):
    """Returns the number of hits / n .

    testR is a dict with an internal UserID as a dict and a list of items as
    values. Normally testR is the second dict split.split returns.
    The list can have a lenght greater than 1.

    recommender is a function which takes an internal UserID and n and returns
    n items recommender for the UserID.

    n is the number of items the recommender can recommend.

    hits = number of items from testR the recommender guessed right.

    See also: "Application of Dimensionality Reduction in Recommender System
    -- A Case Study" by Badrul M. sarcar et al.
    """
    hits = hitrate(testR, recommender, n)[0]
    if n == 0:
        return 0
    return hits / n


def f1(testR, recommender, n):
    """Prints and returns F1 of the recommender.

    testR is a dict with an internal UserID as a dict and a list of items as
    values. Normally testR is the second dict split.split returns.
    The list can have a lenght greater than 1.

    recommender is a function which takes an internal UserID and n and returns
    n items recommender for the UserID.

    n is the number of items the recommender can recommend.

    hits = number of items from testR the recommender guessed right.

    See also: "Application of Dimensionality Reduction in Recommender System
    -- A Case Study" by Badrul M. sarcar et al.
    """
    hits, items = hitrate(testR, recommender, n)
    recall = hits / items
    if recall == 0:
        return 0

    prec = hits / n

    result = ((2 * recall * prec) /
              (recall + prec))
    print("F1: %r" % result)
    return result


def mrhr(testR, recommender, n):
    """Returns the Mean Reciprocal Hitrate of the recommender.

    testR is a dict with an internal UserID as a dict and a list of items as
    values. Normally testR is the second dict split.split returns.
    The list can have a length greater than 1.

    recommender is a function which takes an internal UserID and n and returns
    n items recommender for the UserID.

    n is the number of items the recommender can recommend.

    hits = number of items from testR the recommender guessed right.
    """
    score = 0.0
    items = 0.0
    for u in testR.iterkeys():
        if u % 100 == 0:
            print("%r users tested" % u)
            print("Score so far: %r" % score)

        recs = recommender(u, n)
        if len(recs) > n and not n == -1:
            print("Fatal error: too much recommended items.")

        testSet = set()
        for t in testR[u]:
            testSet.add(t[0])

        for i in testSet:
            if i in recs:
                score += 1.0 / (recs.index(i) + 1)
            items += 1

    print("Score: %r" % score)
    print("Number of possible hits: %r" % items)
    print("Mean Reciprocal Hitrate: %r" % (score / items))
    return score / items


def auc(testR, recommender, r):
    """Returns and prints the AUC of the recommender function.

    testR is a dict with an internal UserID as a dict and a list of items as
    values. Normally testR is the second dict split.split returns.
    The list can have a lenght greater than 1.

    recommender is a function which takes an internal UserID and n and returns
    n items recommender for the UserID.

    r is a reader object with the database read in.

    See also: "BPR: Bayesian Personalized Ranking from Implicit Feedback"
    from Steffen Rendle et al.
    """
    maxIid = r.getMaxIid()

    result = 0
    for u in testR.iterkeys():
        if u % 100 == 0:
            print("%r users tested" % u)
            print("Score so far: %r" % result)
        e = 0.0  # number of items in E
        score = 0  # how often is the hidden item better
        recs = recommender(u, -1)
        for i in testR[u]:
            score += r.getMaxIid() - recs.index(i[0]) - 1
            e += maxIid - 1
        result += score / e
    result /= len(testR.keys())
    print("AUC: %r" % result)
    return result
