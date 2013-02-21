def constant(dbdict):
	dictionary={}
	for data in dbdict.iteritems():
		print data
		if dictionary.has_key(data[1]):
			dictionary[data[1]]+=1
		else:
			dictionary[data[1]]=1

	print dictionary
	max=-1
	item=None
	for tuple in dictionary.iteritems():
		if tuple[1]>max:
			item=tuple[0]
			max=tuple[1]

	return item
