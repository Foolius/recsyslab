import time

def hitrate(testR, recommender,n):
	hits=0.0
	for i in testR:
		for d in recommender(i,n):
			if d[0]==testR[i]:
				hits+=1
				break

	return hits/len(testR)
