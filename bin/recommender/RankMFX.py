def learnModel(n_users, m_items, regU, regI, regJ,
               learningRate, R, k, epochs, numberOfIterations):
    import mf
    return mf.learnModel(n_users, m_items, regU, regI, regJ, learningRate, R,
                         k, epochs, numberOfIterations, mf.hingeLoss,
                         mf.dHingeLoss)
