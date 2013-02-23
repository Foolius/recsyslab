import random

def split(minItems, list, train, val, test):
	random.shuffle(list)
	
	trainList	=	[]
	valList		=	[]
	testList		=	[]

	i=0
	print list

	while list:
		print i
		if i<train:
			trainList.append(list.pop())
		elif i<train+val:
			valList.append(list.pop())
		elif i<train+val+test:
			testList.append(list.pop())
		else:
			i=0
			continue
		i+=1

	print "train: %d"%len(trainList)
	print "val: %d"%len(valList)
	print "test: %d"%len(testList)
	return trainList,valList,testList
