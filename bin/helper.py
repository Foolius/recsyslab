class idOrigDict(object):

	def __init__(self):
		self.orig2id={}
		self.id2orig={}
		self.id=0

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

def writeToFile(reader,toSave,filename):
	f=file(filename,"w")
	for r in toSave.iterkeys():
		ri=reader.getOriginalUid(r)
		for i in toSave[r]:
			ii=reader.getOriginalIid(i)
			f.write("%r\t%r\n"%(ri,ii))
	f.close()
