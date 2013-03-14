def computeDs(R):
	for u in R.getR().iterkeys():
		for i in R.getR()[u]:
			for j in xrange(0,R.getMaxIid()):
				if j in R.getR()[u]:
					continue
				yield u,i,j
