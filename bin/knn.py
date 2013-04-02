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

            for j in xrange(0,matrix.shape[0]):
                self.sim[i,j]=np.dot(matrix.getA()[i],matrix.getA()[j])/(
                    np.sqrt(np.dot(matrix.getA()[i],matrix.getA()[i]))*(
                    np.sqrt(np.dot(matrix.getA()[j],matrix.getA()[j]))))

        print self.sim

    def mostSim(self,u,n):
        scorelist=[]
        for i in xrange(self.sim.shape[0]):
            if i==u:
                continue
            scorelist.append((i,self.sim[u,i]))

        sortedscorelist=sorted(scorelist,
                                    key=lambda(k,v):v,
                                    reverse=True)
        if len(sortedscorelist)<n:
            n=len(sortedscorelist)
        s=set()
        for i in sortedscorelist[:n]:
            s.add(i[0])
        print s
        return s

    def getRec(self,u,n):
        return
