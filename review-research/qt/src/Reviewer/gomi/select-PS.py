

### lib
import sys

### main
i = 0
for line in open(sys.argv[1], "r"):
	if(i == 0):
		pass
		line = line.strip()
		words = line.split(",")
		print line
		#print words[21] # last element
	else:
		line = line.strip()
		words = line.split(",")
		if(words[7] == "0" and words[8] == "0" and words[9] == "0"):
			pass
		else:
			pass
			print line	# 51671

	i += 1
