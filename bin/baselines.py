import grouplensReader

dictionary={}

def __init__():
	for data in grouplensReader.read():
		if dictionary.has_key(data[1]):
			dictionary[data[1]]+=1
		else:
			dictionary[data[1]]=1

def constant():
	max=-1
	item=None
	for tuple in dictionary.iteritems():
		if tuple[1]>max:
			item=tuple[0]
			max=tuple[1]

	return item
