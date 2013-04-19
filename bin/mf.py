import random
import numpy as np
import math


# hinge loss
def hingeLoss(a, y):
    """
    hingeLoss(a, y) = max(0, 1 - a*y)
    """
    z = a * y
    if z > 1:
        return 0
    return 1 - z


def dHingeLoss(a, y):
    """
    -dloss(a,y)/da
    """
    z = a * y
    if z > 1:
        return 0
    return y


def logLoss(a, y):
    """
    logLoss(a, y) = log(1 + exp(-a*y))
    """
    z = a * y
    if z > 18:
        return math.exp(-z)
    if z < -18:
        return -z
    return math.log(1 + math.exp(-z))


def dLogLoss(a, y):
    """
    -dloss(a,y)/da
    """
    z = a * y
    if z > 18:
        return y * math.exp(-z)
    if z < -18:
        return y
    return y / (1 + math.exp(z))

# reg=regularization,R=dict uid=>[ii],T=epochs
#(schedule for learningRate)


def learnModel(n_users, m_items, regU, regI, regJ,
               learningRate, R, k, epochs, numberOfIterations, lossF, dlossF):
    """Learning rate is constant."""
    # MIN_SCALING_FACTOR = 1E-5
    y = 1.0
    # loss = logLoss(0, 0)

    sigma = 0.1
    mu = 0
    # Random initialization of W and H between mean=0 ; sigma=0.1
    W = sigma * np.random.randn(n_users + 1, k) + mu
    H = sigma * np.random.randn(m_items + 1, k) + mu

    printDelay = 0.01 * numberOfIterations
    sum_loss = 0.0
    y = 1.0

    changeU = 1.0 - learningRate * regU
    changeI = 1.0 - learningRate * regI
    changeJ = 1.0 - learningRate * regJ

    eta = learningRate

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
            # the positive example
            userItems = list(R[u])
            i = userItems[np.random.random_integers(0, len(userItems) - 1)]
            # the negative example
            j = np.random.random_integers(0, m_items)
            # if  j is also relevant for u we continue
            # we need to see a negative example to contrast the positive one
            while j in R[u]:
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

            W[u] *= changeU
            H[i] *= changeI
            H[j] *= changeJ

            if dloss != 0.0:
                eta_dloss = learningRate * dloss
                W[u] += eta_dloss * X
                H[i] += eta_dloss * W[u]
                H[j] += eta_dloss * (-W[u])

            t += 1  # increment the iteration
            if t % printDelay == 0:
#                print("Epoch: %i/%i | iteration %i/%i | learning rate=%f"
#                      " | average_loss for the last %i iterations = %f" %
#                     (e + 1, epochs, t, numberOfIterations, eta, printDelay,
#                      sum_loss / printDelay))
                sum_loss = 0.0

    return W, H


def slowlearnModel(n_users, m_items, regU, regI, regJ,
                   learningRate, R, k, epochs, numberOfIterations):
    """slower but the learning rate can change"""
    MIN_SCALING_FACTOR = 1E-5
    y = 1.0
    # loss = logLoss(0, 0)

    sigma = 0.1
    mu = 0
    # Random initialization of W and H between mean=0 ; sigma=0.1
    W = sigma * np.random.randn(n_users, k) + mu
    H = sigma * np.random.randn(m_items, k) + mu

    for e in xrange(0, epochs):
        iter = 0
        print("epoch: %r" % e)
        while iter <= numberOfIterations:
            iter += 1

            u = random.choice(R.keys())

            # if not R.has_key(u):
            #    continue
            if len(R[u]) == 0:
                continue
            # the positive example
            userItems = list(R[u])
            i = userItems[np.random.random_integers(0, len(userItems) - 1)]
            # the negative example
            j = np.random.random_integers(0, m_items)
            # if  j is also relevant for u we continue
            # we need to see a negative example to contrast the positive one
            while j in R[u]:
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
            y = 1.0
            wx = np.dot(W[u], X)
            dloss = dLogLoss(wx, y)

            scaling_factor = 1.0 - (learningRate * regU)
            if scaling_factor > MIN_SCALING_FACTOR:
                W[u] *= (1.0 - learningRate * regU)
            else:
                W[u] *= MIN_SCALING_FACTOR

            scaling_factor = 1.0 - (learningRate * regI)
            if scaling_factor > MIN_SCALING_FACTOR:
                H[i] *= (1.0 - learningRate * regI)
            else:
                H[i] *= MIN_SCALING_FACTOR

            scaling_factor = 1.0 - (learningRate * regJ)
            if scaling_factor > MIN_SCALING_FACTOR:
                H[j] *= (1.0 - learningRate * regJ)
            else:
                H[j] *= MIN_SCALING_FACTOR

            if dloss != 0.0:
                eta_dloss = learningRate * dloss
                W[u] += eta_dloss * X
                H[i] += eta_dloss * W[u]
                H[j] += eta_dloss * (-W[u])

    return W, H
