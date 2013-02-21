class tabSepReader(object):

	R={}
	uidList=[]
	iidList=[]

	def __init__(self,filename):
		dbfile=open(filename,'r')
		
		for line in dbfile:
			split=line.split()
			uid=split[0]
			iid=split[1]
			if not(self.elementInList(self.iidList,iid)):
				self.iidList.append(iid)
			if not(self.elementInList(self.uidList,uid)):
				self.uidList.append(uid)
			if self.uidList.index(uid) in self.R:
				self.R[self.uidList.index(uid)].add(self.iidList.index(iid))
			else:
				self.R[self.uidList.index(uid)]={self.iidList.index(iid)}

	def getR(self):
		return self.R

	def elementInList(self,list, element):
		for i in list:
			if i==element:
				return True
		return False

	def getOriginalUid(self,uid):
		return self.uidList[uid]

	def getOriginalIid(self,iid):
		return self.iidList[iid]


r=tabSepReader("../u.data")
print r.getR()
print r.iidList
print r.getOriginalIid(8)
