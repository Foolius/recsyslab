import helper
import time
class tabSepReader(object):


	def __init__(self,filename):
		self.R={}
		self.uidDict=helper.idOrigDict()
		self.iidDict=helper.idOrigDict()
		self.dbfile=open(filename,'r')
		
		for line in self.dbfile:
			split=line.strip().split()
			origUid=split[0]


			origIid=split[1]
			uid=self.uidDict.add(origUid)
			iid=self.iidDict.add(origIid)
			
			#put in R when not already there
			if uid in self.R:
				self.R[uid].add(iid)
			else:
				self.R[uid]={iid}

	def getR(self):
		return self.R
	
	def getOriginalUid(self,uid):
		return self.uidDict.getOrig(uid)

	def getOriginalIid(self,iid):
		return self.iidDict.getOrig(iid)

	def getMaxIid(self):
		return self.iidDict.id
