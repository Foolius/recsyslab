def learnModel(n_users, m_items, regU, regI, regJ,
        learningRate, R, features, epochs, W = None, H = None): 
    import numpy as np
    import math
    import random

    db = file("u.data","r")

    l=[]
    d={}

    for line in db:
        u,i,r=line.split("\t")[:3]
        u=int(u)
        i=int(i)
        r=int(r)
        l.append((u,i,r))
        d.setdefault(u,{})[i] = r


    MIN_SCALING_FACTOR = 1E-5
    y = 1.0
    np.random.seed(1234567890)
    random.seed(None)

    sigma = 0.1
    mu = 0
    # Random initialization of W and H between mean=0 ; sigma=0.1
    if W == None:
        W = sigma * np.random.randn(n_users + 1, features) + mu
    if H == None:
        H = sigma * np.random.randn(m_items + 1, features) + mu

#    printDelay = int(0.01 * numberOfIterations)
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

    tmpRand = np.random.random_integers
    npdot = np.dot
    mathexp = math.exp
    randomshuffle = random.shuffle

    c =0

    for e in range(0, epochs):
        randomshuffle(l)
        for u, i, r in l:
            # the negative example
            j = tmpRand(0, m_items)
            # if  j is also relevant for u we continue
            # we need to see a negative example to contrast the positive one
            userItems = d[u]
            while userItems.has_key(j):
                j = tmpRand(0, m_items)

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

            # temp
            wu = W[u]
            hi = H[i]
            hj = H[j]

            wx = npdot(wu, X)
            z = wx * y
            if z > 18:
                dloss = y * mathexp(-z)
            elif z < -18:
                dloss = y
            else:
                dloss = y / (1 + mathexp(z))

            #sum_loss += lossF(wx, y)

            if dloss != 0.0:
                # Updates
                eta_dloss = learningRate * dloss

                W[u] += eta_dloss * (hi - hj)
                H[i] += eta_dloss * wu
                H[j] += eta_dloss * (-wu)

                W[u]*= scaling_factorU
                H[i]*= scaling_factorI
                H[j]*= scaling_factorJ
                

                #t += 1  # increment the iteration
                #if t % printDelay == 0:
                #    print("Epoch: %i/%i | iteration %i/%i | learning rate=%f"
                #          " | average_loss for the last %i iterations = %f" %
                #         (e + 1, epochs, t, numberOfIterations, learningRate,
                #          printDelay, sum_loss / printDelay))
                #    sum_loss = 0.0

    return W, H
