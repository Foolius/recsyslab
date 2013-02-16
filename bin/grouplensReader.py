def read():
	file=open('u.data', 'r')

	for line in file:
		split=line.split()
		user=split[0]
		item=split[1]
		yield user,item
