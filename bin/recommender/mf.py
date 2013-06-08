"""Module for Matrix Factorization (mf) techniques.

    learnModel  --  learn a mf model
    MFrec       --  compute recommendations based on a mf model
"""
import random
import numpy as np


# reg=regularization,R=dict uid=>[ii],T=epochs
#(schedule for learningRate)


def learnModel(n_users, m_items, regU, regI, regJ,
               learningRate, R, features, epochs, numberOfIterations, lossF, dlossF):
    """Learns a mf model with a passed loss function.

        n_users             --  The highest internal assigned User ID
        m_items             --  The highest internal assigned Item ID
        regU                --  Regularization for the user vector
        regI                --  Regularization for the positive item
        regJ                --  Regularization for the negative item
        learningRate        --  The learning rate
        R                   --  A dict of the form UserID -> (ItemId, Rating)
        features            --  Number of features of the items and users
        epochs              --  Number of epochs the model should be learned
        numberOfIterations  --  Number of iterations in each epoch
        lossF               --  Loss function
        dlossF              --  Derivation of lossF

    Returns:
        W   --  User Features
        H   --  Item Features

    Based on:
    Steffen Rendle, Christoph Freudenthaler, Zeno Gantner, and
    Lars Schmidt-Thieme. 2009. BPR: Bayesian personalized ranking from
    implicit feedback. In Proceedings of the Twenty-Fifth Conference on
    Uncertainty in Artificial Intelligence (UAI '09).
    AUAI Press, Arlington, Virginia, United States, 452-461.
    """

    """Learning rate is constant."""
    MIN_SCALING_FACTOR = 1E-5
    y = 1.0
    np.random.seed(1234567890)
    # loss = logLoss(0, 0)

    sigma = 0.1
    mu = 0
    # Random initialization of W and H between mean=0 ; sigma=0.1
    W = sigma * np.random.randn(n_users + 1, features) + mu
    H = sigma * np.random.randn(m_items + 1, features) + mu

    printDelay = 0.01 * numberOfIterations
    sum_loss = 0.0
    y = 1.0

    scaling_factorU = 1.0 - (learningRate * regU)
    scaling_factorI = 1.0 - (learningRate * regI)
    scaling_factorJ = 1.0 - (learningRate * regJ)

    if scaling_factorU < MIN_SCALING_FACTOR:
        scaling_factorU = MIN_SCALING_FACTOR
    if scaling_factorI < MIN_SCALING_FACTOR:
        scaling_factorI = MIN_SCALING_FACTOR
    if scaling_factorJ < MIN_SCALING_FACTOR:
        scaling_factorJ = MIN_SCALING_FACTOR

    for e in xrange(0, epochs):
        iter = 0
        t = 0
        while iter <= numberOfIterations:
            iter += 1

            u = random.choice(R.keys())

            # if not R.has_key(u):
            #    continue
            if len(R[u]) == 0:
                continue
            userItems = [x[0] for x in R[u]]
            # the positive example
            i = userItems[np.random.random_integers(0, len(userItems) - 1)]
            # the negative example
            j = np.random.random_integers(0, m_items)
            # if  j is also relevant for u we continue
            # we need to see a negative example to contrast the positive one
#            while [x for x in R[u] if x[0] == j]:
            while j in userItems:
                j = np.random.random_integers(0, m_items)

            X = H[i] - H[j]
            # rank labels
            # positive label :
            # yi = 1.0
            # negative label :
            # yj = 0.0
            # this is equivalent to the sign(yi - yj)
            # y = 1.0 if (yi > yj) else -1.0 if (yi < yj) else 0.0
            # since in this case the positive example is always yi, then y =
            # 1.0
            wx = np.dot(W[u], X)
            dloss = dlossF(wx, y)

            sum_loss += lossF(wx, y)

            # temp
            wu = W[u]
            hi = H[i]
            hj = H[j]

            if dloss != 0.0:
                # Updates
                eta_dloss = learningRate * dloss
                W[u] += eta_dloss * (hi - hj)
                H[i] += eta_dloss * wu
                H[j] += eta_dloss * (-wu)

                W[u] *= scaling_factorU
                H[i] *= scaling_factorI
                H[j] *= scaling_factorJ

            t += 1  # increment the iteration
            if t % printDelay == 0:
                print("Epoch: %i/%i | iteration %i/%i | learning rate=%f"
                      " | average_loss for the last %i iterations = %f" %
                     (e + 1, epochs, t, numberOfIterations, learningRate,
                      printDelay, sum_loss / printDelay))
                sum_loss = 0.0

    return W, H


class MFrec(object):
    """Class to compute recommendations with a mf model."""

    def __init__(self, W, H, trainingR):
        """Initialize the class.

            W           --  Matrix of the User features
            H           --  Matrix of the Item features
            trainingR   --  The dict the model was trained with
        """
        self.W = W
        self.H = H
        self.R = trainingR

    def getRec(self, u, n):
        """
        Returns the n best recommendations for user u based on the mf model.

        Set n = -1 to get all items recommended"""
        scoredict = {}
        for i in range(0, self.H.shape[0]):
            if not i in [x[0] for x in self.R[u]]:
                scoredict[i] = np.dot(self.W[u], self.H[i])

        if n == -1:
            n = len(scoredict)
        import util.helper
        return util.helper.sortList(scoredict.iteritems())[:n]
