#!/usr/bin/python3

### import lib
import sys
import csv
import time
import MySQLdb
from collections import defaultdict
from datetime import datetime

### Init dictionary
diff = defaultdict(lambda: 0)
data_diff = defaultdict(lambda: 0)
FMT = '%Y-%m-%d %H:%M:%S'

### Access into MySQLdb
cnct = MySQLdb.connect(db="qt",user="root", passwd="toshi1126")
cursor = cnct.cursor()
cursor.execute("select ReviewId, PatchSetId, CreatedOn from PatchSet")
lines = cursor.fetchall()
reId = 0
for line in lines:
	if(reId == line[0]):
		if(line[1] == 1):
			second = datetime.strptime(str(line[2]), FMT)
			diff[str(reId)] = second - first
			#print(str(diff[str(reId)].days)+"--"+str(diff[str(reId)].seconds))
			data_diff[str(reId)] = diff[str(reId)].days*24*60*60+diff[str(reId)].seconds
			#print(data_diff[str(reId)])
	else:
		assert line[1] == 0
		reId = line[0]
		first = datetime.strptime(str(line[2]), FMT)

### Read data
header = 0 #top header is label
for row in open(sys.argv[1], "r"):
	if header != 0:
		words = row.split(",")
		#print(words[1]+":"+str(data_diff[words[1]]))
		#print(words[1])
		print(str(data_diff[words[1]]))
	else:
		header = 1

