"""Module to compute the model of Ranking SVD (Sparse SVD)

    Based on:
    Jahrer, Michael, and Andreas Toescher.
    "Collaborative filtering ensemble for ranking."
    Proc. of KDD Cup Workshop at 17th ACM SIGKDD Int. Conf.
    on Knowledge Discovery and Data Mining, KDD. Vol. 11. 2011."""

import random
import numpy as np


def learnModel(n_users, m_items, learningRate, R, features,
               epochs, numberOfIterations):
    """Returns the model of a learned svd as two matrices.

        n_users             --  The highest internal assigned User ID
        m_items             --  The highest internal assigned Item ID
        learningRate        --  The learning rate
        R                   --  A dict of the form UserID -> (ItemId, Rating)
        features            --  Number of features of the items and users
        epochs              --  Number of epochs the model should be learned
        numberOfIterations  --  Number of iterations in each epoch
    """

    sigma = 0.1
    userFeatures = sigma * np.random.randn(n_users + 1, features)
    itemFeatures = sigma * np.random.randn(m_items + 1, features)

    printDelay = 0.1 * numberOfIterations
    sum_loss = 0.0

    import time
    timer = time.clock()

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

            # Choose an item, the user didn't interacted with
            i0 = np.random.random_integers(0, m_items - 1)
            while i0 in userItems:
                i0 = np.random.random_integers(0, m_items - 1)

            # Prediction for the first item
            ruipred = userFeatures[u].dot(itemFeatures[i])
            # Prediction for the second item
            rui0pred = userFeatures[u].dot(itemFeatures[i0])
            rui0 = 0
            for r in R[u]:
                if r[0] == i:
                    rui = r[1]

            dloss = (ruipred - rui0pred) - (rui - rui0)
            sum_loss += dloss
            c = userFeatures[u]
            userFeatures -= learningRate * dloss * (
                itemFeatures[i] - itemFeatures[i0])
            itemFeatures[i] -= learningRate * dloss * c
            itemFeatures[i0] -= learningRate * dloss * (-c)

            t += 1  # increment the iteration
            if t % printDelay == 0:
                timer = time.clock() - timer
                print("Epoch: %i/%i | iteration %i/%i | learning rate=%f"
                      " | average_loss for the last %i iterations = %f"
                      " | time needed: %f" %
                     (e + 1, epochs, t, numberOfIterations, learningRate,
                      printDelay, sum_loss / printDelay, timer))
                     # This is actually not the printing the loss,
                     # but the derivative of the loss.
                sum_loss = 0.0
                timer = time.clock()

    return userFeatures, itemFeatures
