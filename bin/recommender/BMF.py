import numpy as np
import random
import math

#f = open('R.p', 'rb')
#R = cPickle.load(f)
#f.close()
#
#
#mu = 0
#sigma = 0.1
#
#n_users = 45981
#m_items = 11537

def learnModel(n_users, m_items, eta0,BiasLearnRate,BiasReg,RegU,RegI,
        FrequencyRegularization,R,features,epochs,niter):
    """
        eta0    --  learning rate
        BiasLearnRate   --  Bias learning rate
        BiasReg         --  Bias regularization
    """
    avg = 3.74407836255
    min_rating = 1
    rating_range_size = 4

    avg = (avg-min_rating) / rating_range_size;
    global_bias = float(math.log(avg / (1 - avg)))
    np.random.seed(1234567890)
    sigma = 0.1
    mu = 0
    # Random initialization of W and H between mean=0 ; sigma=0.1
    W = sigma * np.random.randn(n_users + 1, features) + mu
    H = sigma * np.random.randn(m_items + 1, features) + mu
    user_bias = sigma * np.random.randn(n_users + 1, 1) + mu
    item_bias = sigma * np.random.randn(m_items + 1, 1) + mu
    users=list(R.keys())
    sum_loss = 0.0
    printDelay = int(math.floor(0.01 * niter))
    for e in xrange(0, epochs):
        iter = 0
        t = 0
        #constant lrate
        eta=eta0
        while iter <= niter:
            iter += 1
            #pick one pair at random (u,i)
            #pick one user at random
            u = random.choice(list(users))
            userItems = [x[0] for x in R[u]]
            # the positive example
            i = userItems[np.random.random_integers(0, len(userItems) - 1)]
            # the negative example
            j = np.random.random_integers(0, m_items)
            # if  j is also relevant for u we continue
            # we need to see a negative example to contrast the positive one
            while j in userItems:
                j = np.random.random_integers(0, m_items)

            for p in R[u]:
                if p[0] == i:
                    rui = p[1]
            rui = int(rui)
            u = int(u)
            i = int(i)
            #
            
            pui = np.dot(W[u],H[i])
            score = global_bias + user_bias[u] + item_bias[i] + pui
            sig_score = 1 / (1 + math.exp(-score))
            pui = min_rating + sig_score * rating_range_size;

            #tmp
            wu = W[u]
            #
            eui = rui - pui
            #
            sum_loss += math.sqrt(eui**2)
            #
            gradient_common = eui * sig_score * (1 - sig_score) * rating_range_size

            #user_reg_weight = float(RegU / math.sqrt(CountByUser[u])) if FrequencyRegularization else RegU
            #item_reg_weight = float(RegI / math.sqrt(CountByItem[i])) if FrequencyRegularization else RegI

            user_reg_weight = RegU
            item_reg_weight = RegI
            
	    #update biases
            user_bias[u] += BiasLearnRate * eta * (gradient_common - BiasReg * user_reg_weight * user_bias[u]) 
            item_bias[i] += BiasLearnRate * eta * (gradient_common - BiasReg * item_reg_weight * item_bias[i]) 

            #adjust latent factors
            u_f = W[u]
            i_f = H[i]
            delta_u = gradient_common * i_f - user_reg_weight * u_f
            W[u] += eta * delta_u

            delta_i = gradient_common * u_f - item_reg_weight * i_f
            H[i] += eta * delta_i

            t += 1 # increment the iteration
            if t % printDelay == 0:
                print("Epoch: %i/%i | iteration %i/%i | learning rate=%f"
                      " | BiasedLR = %f | BiasedReg = %f | RegU = %f | RegI = %f | average_loss for the last %i iterations = %f" %
                     (e + 1, epochs, t, niter, eta, BiasLearnRate,BiasReg,RegU,RegI,
                      printDelay, sum_loss / printDelay))
                sum_loss = 0.0
    return W,H,user_bias,item_bias
