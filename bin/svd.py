import random
import numpy as np


def learnModel(n_users, m_items, learningRate, R, features,
               epochs, numberOfIterations):
    """See pseudocode Collaborative Filtering Ensemble for Ranking."""
    sigma = 0.1
    userFeatures = sigma * np.random.randn(m_items, features)
    itemFeatures = sigma * np.random.randn(m_items, features)

    printDelay = 0.1 * numberOfIterations
    sum_loss = 0.0

    for e in xrange(0, epochs):
        iter = 0
        t = 0
        while iter <= numberOfIterations:
            iter += 1
            # Choose an user randomly
            u = random.choice(R.keys())
            if len(R[u]) == 0:
                continue
            # Choose an item the user interacted with
            userItems = [x[0] for x in R[u]]
            i = random.choice(userItems)

            i0 = np.random.random_integers(0, m_items - 1)
            while i0 in userItems:
                i0 = np.random.random_integers(0, m_items - 1)

            ruipred = userFeatures[u].dot(itemFeatures[i])
            rui0pred = userFeatures[u].dot(itemFeatures[i0])
            rui0 = 0
            for r in R[u]:
                if r[0] == i:
                    rui = r[1]

            loss = (ruipred - rui0pred) - (rui - rui0)
            sum_loss += loss
#            print "userFeatures[u]", userFeatures[u]
#            print "itemFeatures[i]", itemFeatures[i]
#            print "itemFeatures[i0]", itemFeatures[i0]
#            print "ruipred", ruipred
#            print "rui0pred", rui0pred
#            print "rui", rui
#            print "rui0", rui0
#            print "loss", loss
#            print "-----------------"

            from math import isnan
            if isnan(ruipred) or isnan(rui0pred) or isnan(rui) or isnan(
                    rui0) or isnan(loss):
                raise NameError

            for k in xrange(0, features):
                c = userFeatures[u, k]
                userFeatures[u, k] -= learningRate * (loss * (
                    itemFeatures[i, k] - itemFeatures[i0, k]))
                itemFeatures[i, k] -= learningRate * (loss * c)
                itemFeatures[i0, k] -= learningRate * (loss * (-c))

            scalingFactor = 1E-3
            userFeatures[u] *= scalingFactor
            itemFeatures[i] *= scalingFactor
            itemFeatures[i0] *= scalingFactor

            t += 1  # increment the iteration
            if t % printDelay == 0:
                print("Epoch: %i/%i | iteration %i/%i | learning rate=%f"
                      " | average_loss for the last %i iterations = %f" %
                     (e + 1, epochs, t, numberOfIterations, learningRate,
                      printDelay, sum_loss / printDelay))
                sum_loss = 0.0

    return userFeatures, itemFeatures
