#!/bin/sed

# uml.sed is used to change umlaute to LaTeX-code
# it can be used like this
# sed -f uml.sed old.tex > new.tex

s/ä/\\"{a}/g
s/ö/\\"{o}/g
s/ü/\\"{u}/g
s/Ä/\\"{A}/g
s/Ö/\\"{O}/g
s/Ü/\\"{U}/g
s/ß /\\ss{} /g
s/ß/\\ss /g
