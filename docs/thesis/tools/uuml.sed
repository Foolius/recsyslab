#!/bin/sed

# uml.sed is used to change LaTeX-code to umlaute
# it can be used like this
# sed -f uml.sed old.tex > new.tex

s/\\"{a}/ä/g
s/\\"{o}/ö/g
s/\\"{u}/ü/g
s/\\"{A}/Ä/g
s/\\"{O}/Ö/g
s/\\"{U}/Ü/g
s/\\ss /ß/g
s/\\ss{}/ß/g
