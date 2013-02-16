def read():
	file=open('u.data', 'r')

	for line in file:
		yield line
