import numpy as np
import helper

class knn(object):
    def __init__(self, matrix):
        self.sim=np.zeros((matrix.shape[1],matrix.shape[1]))
        self.itemUserMatrix=matrix.transpose()
        count=0
        print self.sim.shape
        for i in xrange(0,self.sim.shape[1]):
            if count%100==0:
                print("%r Similarities calculated"%count)
            count+=1

            for j in xrange(0,self.sim.shape[1]):
                self.sim[i,j]=self.cos(self.itemUserMatrix[i],self.itemUserMatrix[j])

    def cos(self,a,b):
        """gets two vectors(onedimensional np.matrix)
        and computes their cosine"""
        return np.dot(a.getA()[0],b.getA()[0])/(
            np.sqrt(np.dot(a.getA()[0],a.getA()[0]))*(
            np.sqrt(np.dot(b.getA()[0],b.getA()[0]))))


    def mostSim(self,item,n):
        """Returns the n most similar items for item."""
        scorelist=[]
        for i in xrange(self.sim.shape[0]):
            if i==item:
                continue
            scorelist.append((i,self.sim[item,i]))

        return helper.listToSet(helper.sortList(scorelist),n)

    def simToSet(self,itemSet,item,n):
        """Returns the sum of the similarities of itemSet and item.
        not exactly like in the paper because I'm adding up all items 
        in the set and not only n."""
        simsum=0.
        for s in itemSet:
            simsum+=self.sim[s,item]
        return simsum


    def getRec(self,u,n):
        """Returns the n best recommendations for user u"""
        U=set() #items the user bought
        C=set() #items similar to items the items of u
        for j in xrange(0,self.sim.shape[1]):
            if self.itemUserMatrix[j,u]:
                U.add(j)
                C=C.union(self.mostSim(j,n))
        C=C.difference(U)
        l=[]
        for c in C:
            l.append((c,self.simToSet(U,c,n)))

        return helper.listToSet(helper.sortList(l),n)
