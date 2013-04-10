import numpy as np
import random

# we are going to ignore the bias term for the moment


class RankMFX:
    def learnModel(self, n_users, m_items, regU, regI, regJ,
                   learningRate, R, k, epochs, niter):
        # MIN_SCALING_FACTOR = 1E-5
        np.random.seed(1234567890)

        # Random initialization of W and H between mean=0 ; sigma=0.1
        sigma = 0.1
        mu = 0
        W = sigma * np.random.randn(n_users, k) + mu
        H = sigma * np.random.randn(m_items, k) + mu
        #---
        # This is slower if R is big, i.e., close to the number of users, but
        # for the online approach is faster
        userIds = R.keys()

        printDelay = 0.01 * niter
        sum_loss = 0
        y = 1.0

        changeU = 1.0 - learningRate * regU
        changeI = 1.0 - learningRate * regI
        changeJ = 1.0 - learningRate * regJ

        for epoch in xrange(0, epochs):
            t = 1  # iteration
            while t <= niter:
                # constant learning rate :
                eta = learningRate

                u = random.choice(userIds)

                # if not R.has_key(u):
                #    continue
                if len(R[u]) == 0:
                    continue
                # the positive example
                userItems = list(R[u])
                i = userItems[np.random.random_integers(0, len(userItems) - 1)]
                # the negative example
                j = np.random.random_integers(0, m_items - 1)
                # if  j is also relevant for u we continue
                # we need to see a negative example to contrast the positive
                # one
                while j in R[u]:
                    j = np.random.random_integers(0, m_items - 1)

                # The features difference between the sampled items
                X = H[i] - H[j]

                # rank labels
                # positive label :
                # yi = 1.0
                # negative label :
                # yj = 0.0
                # this is equivalent to the sign(yi - yj)
                # y = 1.0 if (yi > yj) else -1.0 if (yi < yj) else 0.0
                # since in this case the positive example is always yi, then y
                # = 1.0

                # for the moment the bias term is ignored
                wx = np.dot(W[u], X)

                dloss = self.dHingeLoss(wx, y)

                # for debugging.  The sum of the loss:
                sum_loss += self.hingeLoss(wx, y)

                # factors update and regularization
                # always regularize:
                W[u] *= changeU
                H[i] *= changeI
                H[j] *= changeJ

                if dloss != 0.0:
                    eta_dloss = eta * dloss
                    W[u] += eta_dloss * X
                    H[i] += eta_dloss * W[u]
                    H[j] += eta_dloss * (-W[u])

                t += 1  # increment the iteration
                if t % printDelay == 0:
                    print("Epoch: %i/%i | iteration %i/%i | learning rate=%f"
                          " | average_loss for the last %i iterations = %f" %
                         (epoch + 1, epochs, t, niter, eta, printDelay,
                          sum_loss / printDelay))
                    sum_loss = 0.0
        return W, H

    def slowlearnModel(self, n_users, m_items, reg_u, reg_i, reg_j,
                       eta0, R, k, epochs, niter):
        """slower but the learning rate can change"""
        MIN_SCALING_FACTOR = 1E-5
        np.random.seed(1234567890)

        # Random initialization of W and H between mean=0 ; sigma=0.1
        sigma = 0.1
        mu = 0
        W = sigma * np.random.randn(n_users, k) + mu
        H = sigma * np.random.randn(m_items, k) + mu
        #---
        # This is slower if R is big, i.e., close to the number of users, but
        # for the online approach is faster
        userIds = R.keys()

        printDelay = 0.01 * niter
        sum_loss = 0

        for epoch in xrange(0, epochs):
            t = 1  # iteration
            while t <= niter:
                # constant learning rate :
                eta = eta0

                u = random.choice(userIds)

                # if not R.has_key(u):
                #    continue
                if len(R[u]) == 0:
                    continue
                # the positive example
                userItems = list(R[u])
                i = userItems[np.random.random_integers(0, len(userItems) - 1)]
                # the negative example
                j = np.random.random_integers(0, m_items - 1)
                # if  j is also relevant for u we continue
                # we need to see a negative example to contrast the positive
                # one
                while j in R[u]:
                    j = np.random.random_integers(0, m_items - 1)

                # The features difference between the sampled items
                X = H[i] - H[j]

                # rank labels
                # positive label :
                # yi = 1.0
                # negative label :
                # yj = 0.0
                # this is equivalent to the sign(yi - yj)
                # y = 1.0 if (yi > yj) else -1.0 if (yi < yj) else 0.0
                # since in this case the positive example is always yi, then y
                # = 1.0
                y = 1.0

                # for the moment the bias term is ignored
                wx = np.dot(W[u], X)

                dloss = self.dHingeLoss(wx, y)

                # for debugging.  The sum of the loss:
                sum_loss += self.hingeLoss(wx, y)

                # factors update and regularization
                # always regularize:
                scaling_factor = 1.0 - (eta * reg_u)
                if scaling_factor > MIN_SCALING_FACTOR:
                    W[u] *= (1.0 - eta * reg_u)
                else:
                    W[u] *= MIN_SCALING_FACTOR

                scaling_factor = 1.0 - (eta * reg_i)
                if scaling_factor > MIN_SCALING_FACTOR:
                    H[i] *= (1.0 - eta * reg_i)
                else:
                    H[i] *= MIN_SCALING_FACTOR

                scaling_factor = 1.0 - (eta * reg_j)
                if scaling_factor > MIN_SCALING_FACTOR:
                    H[j] *= (1.0 - eta * reg_j)
                else:
                    H[j] *= MIN_SCALING_FACTOR

                if dloss != 0.0:
                    eta_dloss = eta * dloss
                    W[u] += eta_dloss * X
                    H[i] += eta_dloss * W[u]
                    H[j] += eta_dloss * (-W[u])

                t += 1  # increment the iteration
                if t % printDelay == 0:
                    print("Epoch: %i/%i | iteration %i/%i | learning rate=%f"
                          + "| average_loss for the last %i iterations = %f" %
                          (epoch + 1, epochs, t, niter, eta, printDelay,
                              sum_loss / printDelay))
                    sum_loss = 0.0
        return W, H

    # hinge loss
    def hingeLoss(self, a, y):
        """
        hingeLoss(a, y) = max(0, 1 - a*y)
        """
        z = a * y
        if z > 1:
            return 0
        return 1 - z

    def dHingeLoss(self, a, y):
        """
        -dloss(a,y)/da
        """
        z = a * y
        if z > 1:
            return 0
        return y
