import time
import numpy as np

def hitrate(testR, recommender,n):
	hits=0.0
	items=0.0
	for u in testR.iterkeys():
		#print("recommender:")
		#print(recommender(u,n))
		#print("testR")
		#print(testR[u])
		if u%100==0:
			print("%r users tested"%u)
			print("Hits so far: %r"%hits)
		hits+=len(recommender(u,n).intersection(testR[u]))
		items+=len(testR[u])

	print("Number of hits: %r"%hits)
	print("Number of recommended items: %r"%items)
	return hits/items

class MFtest(object):

	def __init__(self,W,H,trainingR):
		self.W=W
		self.H=H
		self.R=trainingR
		#print(self.R)

	def	getRec(self,u,n):
		scoredict={}
		for i in range(0,self.H.shape[0]):
			if not i in self.R[u]:
				scoredict[i]=np.dot(self.W[u],self.H[i])
				#print("scoredict[%r]: %r"%(i,scoredict[i]))
	
		sortedscorelist=sorted(scoredict.iteritems(),
									key=lambda(k,v):v,
									reverse=True)
		if len(sortedscorelist)<n:
			n=len(sortedscorelist)
		s=set()
		for i in sortedscorelist[:n]:
			s.add(i[0])
		return s
