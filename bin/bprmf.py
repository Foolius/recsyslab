import random
import numpy as np
import math

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
    
#reg=regularization,R=dict uid=>[ii],T=epochs
#(schedule for learningRate)
def learnModel(n_users,m_items,regU,regI,regJ,learningRate,R,k,epochs,numberOfIterations):
    MIN_SCALING_FACTOR = 1E-5
    y = 1.0
    loss=logLoss(0,0)

    sigma=0.1
    mu=0
    #Random initialization of W and H between mean=0 ; sigma=0.1
    W = sigma * np.random.randn(n_users, k) + mu
    H = sigma * np.random.randn(m_items, k) + mu
    y = 1.0

    changeU=1.0-learningRate*regU
    changeI=1.0-learningRate*regI
    changeJ=1.0-learningRate*regJ

    for e in xrange(0,epochs):
        iter=0
        print("epoch: %r"%e)
        while iter<=numberOfIterations:
            iter+=1

            u = random.choice(R.keys())

            #if not R.has_key(u):
            #    continue
            if len(R[u]) == 0:
                continue
            #the positive example 
            userItems = list(R[u])
            i = userItems[np.random.random_integers(0, len(userItems)-1)]
            #the negative example
            j = np.random.random_integers(0, m_items-1)
            #if  j is also relevant for u we continue 
            #we need to see a negative example to contrast the positive one
            while j in R[u]:
                j = np.random.random_integers(0, m_items-1)

            X = H[i] - H[j]
            #rank labels
            #positive label :
            #yi = 1.0
            #negative label :
            #yj = 0.0
            #this is equivalent to the sign(yi - yj)
            #y = 1.0 if (yi > yj) else -1.0 if (yi < yj) else 0.0
            #since in this case the positive example is always yi, then y = 1.0 
            wx = np.dot(W[u],X)
            dloss=dLogLoss(wx,y)

            W[u] *= changeU
            H[i] *= changeI
            H[j] *= changeJ
                        
            if dloss != 0.0 :
                eta_dloss = learningRate * dloss
                W[u] += eta_dloss * X
                H[i] += eta_dloss * W[u]
                H[j] += eta_dloss * (-W[u])
                    
    return W,H





def slowlearnModel(n_users,m_items,regU,regI,regJ,learningRate,R,k,epochs,numberOfIterations):
    """slower but the learning rate can change"""
    MIN_SCALING_FACTOR = 1E-5
    y = 1.0
    loss=logLoss(0,0)

    sigma=0.1
    mu=0
    #Random initialization of W and H between mean=0 ; sigma=0.1
    W = sigma * np.random.randn(n_users, k) + mu
    H = sigma * np.random.randn(m_items, k) + mu
    
    for e in xrange(0,epochs):
        iter=0
        print("epoch: %r"%e)
        while iter<=numberOfIterations:
            iter+=1

            u = random.choice(R.keys())

            #if not R.has_key(u):
            #    continue
            if len(R[u]) == 0:
                continue
            #the positive example 
            userItems = list(R[u])
            i = userItems[np.random.random_integers(0, len(userItems)-1)]
            #the negative example
            j = np.random.random_integers(0, m_items-1)
            #if  j is also relevant for u we continue 
            #we need to see a negative example to contrast the positive one
            while j in R[u]:
                j = np.random.random_integers(0, m_items-1)

            X = H[i] - H[j]
            #rank labels
            #positive label :
            #yi = 1.0
            #negative label :
            #yj = 0.0
            #this is equivalent to the sign(yi - yj)
            #y = 1.0 if (yi > yj) else -1.0 if (yi < yj) else 0.0
            #since in this case the positive example is always yi, then y = 1.0 
            y = 1.0
            wx = np.dot(W[u],X)
            dloss=dLogLoss(wx,y)

            scaling_factor = 1.0 - (learningRate * regU)
            if scaling_factor > MIN_SCALING_FACTOR :
                W[u] *= (1.0 - learningRate * regU)  
            else:
                W[u] *= MIN_SCALING_FACTOR

            scaling_factor = 1.0 - (learningRate * regI)
            if scaling_factor > MIN_SCALING_FACTOR :
                H[i] *= (1.0 - learningRate * regI)  
            else:
                H[i] *= MIN_SCALING_FACTOR

            scaling_factor = 1.0 - (learningRate * regJ)
            if scaling_factor > MIN_SCALING_FACTOR :
                H[j] *= (1.0 - learningRate * regJ)  
            else:
                H[j] *= MIN_SCALING_FACTOR
                        
            if dloss != 0.0 :
                eta_dloss = learningRate * dloss
                W[u] += eta_dloss * X
                H[i] += eta_dloss * W[u]
                H[j] += eta_dloss * (-W[u])
                    
    return W,H
