class idOrigDict(object):
	orig2id={}
	id2orig={}
	id=0

	def add(self,orig):
		if not orig in self.orig2id.keys():
			self.orig2id[orig]=self.id
			self.id2orig[self.id]=orig
			self.id+=1
		return self.getId(orig)
	
	def getOrig(self,id):
		return self.id2orig[id]

	def getId(self,orig):
		return self.orig2id[orig]
