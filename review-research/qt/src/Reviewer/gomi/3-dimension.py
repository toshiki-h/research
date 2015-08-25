###

###
import csv
import sys
from collections import defaultdict

###
dic = defaultdict(lambda: 0)

f = 0
for line in open(sys.argv[1], "r"):
	words = line.split(",")
	if(f == 0):
		#print(words[7]+","+words[9])
		f = 1
	else:
		key = str(words[7])+","+str(words[9])
		dic[key] += 1

#print "NumPositive,NumNegative,Frequancy"
for k in dic:
	print str(k)+","+str(dic[k])
