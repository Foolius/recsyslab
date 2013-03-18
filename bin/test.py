import time
import numpy as np

def hitrate(testR, recommender,n):
	hits=0.0
	items=0.0
	for i in testR:
		hits+=len(recommender(i,n).intersection(testR[i]))
		items+=len(recommender(i,n))

	return hits/items

class svdtest(object):

	def __init__(self,W,H):
		self.W=W
		self.H=H

	def	getRec(self,u,n):
		scoredict={}
		for i in range(0,self.H.shape[0]):
			scoredict[i]=np.dot(self.W[u],self.H[i])
	
		sortedscorelist=sorted(scoredict.iteritems(),
									key=lambda(k,v):v,
									reverse=True)
		if len(sortedscorelist)<n:
			n=len(sortedscorelist)
		s=set()
		for i in sortedscorelist:
			s.add(i[0])
		return s
