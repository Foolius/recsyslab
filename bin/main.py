import evaluation
import reader

r=reader.tabSepReader("../u.data")

print evaluation.split(0,r.getSimpleList(),3,1,1)
