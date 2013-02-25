class constant(object):
	
	dictionary={}
	sortedList=[]

	def __init__(self,dbdict):
		for data in dbdict.iteritems():
			for item in iter(data[1]):
				if self.dictionary.has_key(item):
					self.dictionary[item]+=1
				else:
					self.dictionary[item]=1

		self.sortedList=sorted(self.dictionary.iteritems(),
								key=lambda (k,v):v,
								reverse=True)
	def getRec(self,user,n):
		if len(self.sortedList)<n:
			n=len(self.sortedList)

		return self.sortedList[:n]
