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

#			print("reader: %r"%origUid)
#			time.sleep(1.0)

			origIid=split[1]
			print("uidDict:")	
			uid=self.uidDict.add(origUid)
			print("iidDict:")	
			iid=self.iidDict.add(origIid)
			
			#put in R when not already there
			if uid in self.R:
				self.R[uid].add(iid)
			else:
				self.R[uid]={iid}
			time.sleep(1.4)

	def getR(self):
		return self.R
	
	def getOriginalUid(self,uid):
		return self.uidDict.getOrig(uid)

	def getOriginalIid(self,iid):
		return self.iidDict.getOrig(iid)
