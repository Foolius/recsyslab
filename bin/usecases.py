# Reading a database file
import reader
r = reader.tabSepReader(<filename>)

# Get recommendations with simple algorithms
import primitive
rand = primitive.randomRec(r.getR())
rand.getRec(r.
