import evaluation
import reader
import baselines
import test

r=reader.tabSepReader("../kleinu.data")
split=evaluation.split(r.getR())
print r.getR()
print split
