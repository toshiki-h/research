##############################################
# file		: my_data_middle.sh				 
# author	: toshiki hirao			 
# e-mail	: hirao.toshiki.ho7@is.naist.jp	 
# date		: 2015/06/11				
# upsate	: 2015/06/11	 
# summary	: ReviewId,OwnerId,Status,CreatedOn,LastUpdatedOn,TimeOfDifference,NumberOfPatches
##############################################


import sys
import csv
import MySQLdb
from datetime import datetime

### make data_file.csv
f_id = open(sys.argv[1], "r")
f_w = open("Ihara_data_set.list", "a")

### Access MySQL
connector = MySQLdb.connect(db="qt",user="root", passwd="toshi1126")
cursor = connector.cursor()

FMT = '%Y-%m-%d %H:%M:%S'
for Id in f_id:
	### Select ReviewId and CreatedOn
	cursor.execute("select ReviewId,OwnerId,Status,CreatedOn,LastUpdatedOn,NumberOfPatches from Review where ReviewId = "+Id)
	rows = cursor.fetchall()
	for row in rows:
		#print str(row[3])+" - "+str(row[4])
		start = str(row[3])
		end = str(row[4])
		diff = datetime.strptime(str(row[4]), FMT) - datetime.strptime(str(row[3]), FMT)
		#print "%d = %i sec." % (row[0], diff.days*24*60*60+diff.seconds)
		print str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+","+str(row[4])+","+str(diff.days*24*60*60+diff.seconds)+","+str(row[5])
		## ReviewId,OwnerId,Status,CreatedOn,LastUpdatedOn,TimeOfDifference,NumberOfPatches

