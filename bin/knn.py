import numpy as np

class knn(object):
    def __init__(self, matrix):
        self.sim=np.zeros((matrix.shape[1],matrix.shape[1]))
        self.matrix=matrix
        count=0
        for i in xrange(0,matrix.shape[1]):
            if count%100==0:
                print("%r Similarities calculated"%count)
            count+=1

            for j in xrange(0,matrix.shape[1]):
                self.sim[i,j]=np.dot(matrix.getA()[i],matrix.getA()[j])/(
                    np.sqrt(np.dot(matrix.getA()[i],matrix.getA()[i]))*(
                    np.sqrt(np.dot(matrix.getA()[j],matrix.getA()[j]))))


    def mostSim(self,item,n):
        """Returns the n most similar items for item."""
        scorelist=[]
        for i in xrange(self.sim.shape[0]):
            if i==item:
                continue
            scorelist.append((i,self.sim[item,i]))

        sortedscorelist=sorted(scorelist,
                                    key=lambda(k,v):v,
                                    reverse=True)
        if len(sortedscorelist)<n:
            n=len(sortedscorelist)
        s=set()
        for i in sortedscorelist[:n]:
            s.add(i[0])
        return s

    def simToset(self,itemSet,item,n):
        """Returns the sum of the similarities of itemSet and item."""
        simsum=0.
        for s in itemSet:
            simsum+=self.sim[s,item]
        return simsum


    def getRec(self,u,n):
        """Returns the n best recommendations for user u"""
        return
