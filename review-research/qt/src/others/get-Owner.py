#!/usr/bin/python3

### import library
import sys
import csv
import MySQLdb
from datetime import datetime

### open file
f = open(sys.argv[1], "r")

### access db
cnct = MySQLdb.connect(db="qt",user="root", passwd="toshi1126")
cursor = cnct.cursor()

### ectract Owner Id
i = 1
for row in f:
	## read ReviewId, PersonId, CreateOnDate
	if i > 1:
		row = row.strip()
		clm = row.split(",")
		#if i < 5:	## check
		#	print(clm)
		review_id = clm[1]
		owner_id = clm[2]
		create_date = clm[4]
		#print(review_id+" "+owner_id+" "+create_date)
		## select from qt
		cursor.execute("select ReviewId, OwnerId, LastUpdatedOn, Status from Review where OwnerId = '"+owner_id+"' and LastUpdatedOn < '"+create_date+"' and Status = 'merged';")
		lines = cursor.fetchall()
		print(row+","+str(sum(1 for n in lines)))
	else:
		print(row.strip()+",exp")
	i += 1
