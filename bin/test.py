def hitrate(testR, recommender,n):
	hits=0.0
	for i in testR:
		for d in recommender(i[0],n):
			#print "d: %s i: %s"%(d[1],i[1])
			if d[1]==i[1]:
				hits+=1
				break

	return hits/len(testR)
