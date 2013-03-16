import random
import numpy as np

def computeDs(R):
	ds=[]
	for u in R.getR().iterkeys():
		for i in R.getR()[u]:
			for j in xrange(0,R.getMaxIid()):
				if j in R.getR()[u]:
					continue
				ds.append((u,i,j))
	random.shuffle(ds)
	return ds

def foo(k,R):
	H=np.matrix(np.random.randint(
		0,2,k*R.getMaxIid()).
		reshape(R.getMaxIid(),k))

	W=np.matrix(np.random.randint(
		0,2,k*R.getMaxUid()).
		reshape(R.getMaxUid(),k))

	def xui(u,i):
		#getA() gives an array in an array so [0]
		dot=np.dot(W[u].getA()[0],H[i].getA()[0])
		print dot
		return dot

	def xuij(u,i,j):
		return xui(u,i)-xui(u,j)

	def dxuij(u,i,j,theta):
		return 0
