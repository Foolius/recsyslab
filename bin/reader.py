import helper

class tabSepReader(object):

	R={}
	simpleList=[]
	uidList=[]
	iidList=[]
	uidDict=helper.idOrigDict()
	iidDict=helper.idOrigDict()

	def __init__(self,filename):
		dbfile=open(filename,'r')
		
		for line in dbfile:
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
		print("getor")
		return self.uidDict.getOrig(uid)

	def getOriginalIid(self,iid):
		return self.iidDict.getOrig(iid)
