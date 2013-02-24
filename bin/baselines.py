def constant(dbdict,n):
	dictionary={}
	for data in dbdict.iteritems():
		for item in iter(data[1]):
			if dictionary.has_key(item):
				dictionary[item]+=1
			else:
				dictionary[item]=1

	sortedList=sorted(dictionary.iteritems(),
							key=lambda (k,v):v,
							reverse=True)

	if len(sortedList)<n:
		n=len(sortedList)

	return sortedList[:n]
