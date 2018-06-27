import sys
file = sys.argv[1]
def remLine():
	fr = open(file)
	contents = fr.readlines()
	fr.close()
	fw = open(file,'w')
	contents[0] = " "
	contents[1] = " "
	contents = "".join(contents)
	fw.write(contents)
	fw.close()

def countLines():
	fr = open(file)
	n=0
	for line in fr:
		n=n+1
	fr.close()
	return n

def remTime():
	fr = open(file)
	contents = fr.readlines()
	fr.close()
	n = countLines()
	fw = open(file,'w')
	#print n
	for i in range(0,n):
		#print i
		contents[i]= contents[i].split("Prashant:")[1]
		contents[i]= contents[i].split("  ")[1]
		contents[i] = ": L"+contents[i]
		contents[i]= contents[i].replace('.','/')
	contents = "".join(contents)
	fw.write(contents)
	fw.close()
		
remLine()	
remTime()

