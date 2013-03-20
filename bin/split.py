import random
import copy

def split(R,seed):

	random.seed(seed)
	split={}
	training={}

	for user in R.iterkeys():
		item=random.sample(R[user],1)[0] #because random.sample gives a list
		split[user]=set([item])
		s=copy.deepcopy(R[user])
		s.discard(item)
		training[user]=s
	return training,split
