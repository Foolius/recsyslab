def grouplensReader(filename):

	dbfile=open(filename,'r')
	dbdict={}
	
	for line in dbfile:
		print line
		split=line.split()
		dbdict[split[0]]=split[1]
	
	return dbdict
