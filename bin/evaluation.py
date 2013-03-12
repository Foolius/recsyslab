import random

def split(R):

	split={}

	for user in R.iterkeys():
		item=random.sample(R[user],1)[0] #because random.sample gives a list
		split[user]=item
		R[user].discard(item)
	return R,split
