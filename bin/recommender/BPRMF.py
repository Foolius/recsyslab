import math


def learnModel(n_users, m_items, regU, regI, regJ,
               learningRate, R, features, epochs, numberOfIterations):
    """Learns a model with the BPRMF algorithm, actually just calls mf.

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
    import mf
    return mf.learnModel(n_users, m_items, regU, regI, regJ, learningRate, R,
                         features, epochs, numberOfIterations, logLoss,
                         dLogLoss)


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
    Derivative of the logLoss.
    """
    z = a * y
    if z > 18:
        return y * math.exp(-z)
    if z < -18:
        return y
    return y / (1 + math.exp(z))
