import random
import numpy as np


def learnModel(n_users, m_items, learningRate, R, features,
               epochs, numberOfIterations):
    """See pseudocode Collaborative Filtering Ensemble for Ranking."""
    sigma = 0.1
    userFeatures = sigma * np.random.randn(m_items, features)
    itemFeatures = sigma * np.random.randn(m_items, features)

    for e in xrange(0, epochs):
        while iter <= numberOfIterations:
            # Choose an user randomly
            u = random.choice(R.keys())
            if len(R[u]) == 0:
                continue
            # Choose an item the user interacted with
            i = random.choice(R[u])

            i0 = np.random.random_integers(0, m_items)
            while i0 in R.getR()[u]:
                i0 = np.random.random_integers(0, m_items)

            ruipred = userFeatures[u].dot(itemFeatures[i])
            rui0pred = userFeatures[u].dot(itemFeatures[i0])
            rui0 = 0
            e = (ruipred - rui0pred) - (userItemMatrix[u, i] - rui0)


            for k in xrange(0, features):
                c = userFeatures[u, k]
                userFeatures[u, k] -= learningRate * (e * (
                    itemFeatures[i, k] - itemFeatures[i0, k]))
                itemFeatures[i, k] -= learningRate * (e * c)
                itemFeatures[i0, k] -= learnModel * (e * (-c))

    return userFeatures, itemFeatures
