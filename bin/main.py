import evaluation
import reader
import baselines

r=reader.tabSepReader("../u.data")

print baselines.constant(r.getR(),10)
