import grouplensReader

i=0
for line in grouplensReader.read():
	i+=1
	if i>10:
		break
	print line
