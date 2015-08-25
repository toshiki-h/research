##############################################
# Author	: Toshiki Hirao
# Update	: 2015/07/14
# Summary	: This calcurate a percentage of 
#			  comments which was written by patch owner.					 
##############################################

### import lib
import sys
import csv
import MySQLdb
from collections import defaultdict

### Define functions
def IsAutoTest(author):
	# 1000049 -> Qt Sanity Bot
	# -1 	  -> Gerrit System
	# 1000060 -> Qt Continuous Integration System
	# 1000191 -> Qt Submodule Update Bot
	# 1002169 -> Qt Doc Bot
	if(author == 1000049 or author == -1 or author == 1000060 or author == 1000191 or author == 1002169):
		return 1	## The author is Auto Test.
	else:
		return 0

### Main process
### Read ReviewId, PatchOwnerId
i = 0
id_List = []
own_List = []
for row in open(sys.argv[1], "r"):
	if i > 0:
		words = row.split(",")
		id_List.append(words[0])
		own_List.append(words[1])
	else:
		pass
	i += 1
assert len(id_List) == len(own_List)

### Access MySQL
cnct = MySQLdb.connect(db="qt",user="root", passwd="toshi1126")
csr = cnct.cursor()

i = 0
for (rev_Id, own_Id) in zip(id_List, own_List):
	csr.execute("select ReviewId, Message, AuthorId from Comment where ReviewId = "+rev_Id+" and Message like 'Patch Set 1:%';")
	lines = csr.fetchall()

	all_ct = 0
	own_ct = 0
	for line in lines: # Investigate each comment
		assert rev_Id == str(line[0])
		message = str(line[1].replace("\n", " "))
		author = line[2]
		#print message
		if(IsAutoTest(author) != 1): # If message-author isn't auto test system, it counts the number of comments.
			all_ct += 1
			if own_Id == str(author):
				own_ct += 1
	if (all_ct > 0): 
		per = float(own_ct) / float(all_ct)
		print str(own_ct)+","+str(per)
		#print str(rev_Id) + " -> "+str(own_ct)+" / "+str(all_ct)+" = "+str(per)
	else:
		print str(own_ct)+","+str(0)
		#print str(rev_Id) + " -> "+str(own_ct)+" / "+str(all_ct)+" = " + str(0)
