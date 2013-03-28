import random

class constant(object):

    def __init__(self,dbdict):
        self.dictionary={}
        self.sortedList=[]
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
        s=set()
        for i in self.sortedList[:n]:
            s.add(i[0])
        return s

class randomRec(object):
    def __init__(self,dbdict):
        self.maxIid=0
        for data in dbdict.iteritems():
            for item in iter(data[1]):
                if item>self.maxIid:
                    self.maxIid=item

    def getRec(self,user,n):
        return set(random.sample(range(self.maxIid),n))
