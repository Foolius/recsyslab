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

def writeOrigToFile(reader,toSave,filename):
    f=file(filename,"w")
    for r in toSave.iterkeys():
        ri=reader.getOriginalUid(r)
        for i in toSave[r]:
            ii=reader.getOriginalIid(i)
            f.write("%r\t%r\n"%(ri,ii))
    f.close()

def writeInternalToFile(reader,toSave,filename):
    f=file(filename,"w")
    for r in toSave.iterkeys():
        for i in toSave[r]:
            f.write("%r\t%r\n"%(r,i))
    f.close()


def sortResults(name):
    infile=open(name,'r')
    outfile=open("out"+name,'w')
    b=True
    l=[]
    for line in infile:
        if line[0]=="S": 
            outfile.write(line)
            continue
        if line[0]=="A":
            if b:
                outfile.write(line)
            b=False
            continue
        l.append(line.strip().split("|",-1))
    l=sorted(l,key=lambda(a,b,c,d,e):e,reverse=True)
    
    for e in l:
        outfile.write("|".join(e))
        outfile.write("\n")
        print("|".join(e))

        #outfile.write(e)

    outfile.close()
    infile.close()
    
#sortResults("RankMFXresults.data")
