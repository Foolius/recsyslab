def learnModel(n_users, m_items, regU, regI, regJ,
               learningRate, R, k, epochs, numberOfIterations):
    """Learns a model with the RankMFX algorithm, actually just calls mf.

        n_users             --  The highest internal assigned User ID
        m_items             --  The highest internal assigned Item ID
        regU                --  Regularization for the user vector
        regI                --  Regularization for the positive item
        regJ                --  Regularization for the negative item
        learningRate        --  The learning rate
        R                   --  A dict of the form UserID -> (ItemId, Rating)
        k                   --  Number of features of the items and users
        epochs              --  Number of epochs the model should be learned
        numberOfIterations  --  Number of iterations in each epoch

    Returns:
        W   --  User Features
        H   --  Item Features
    """
    import mf
    return mf.learnModel(n_users, m_items, regU, regI, regJ, learningRate, R,
                         k, epochs, numberOfIterations, hingeLoss,
                         dHingeLoss)


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
