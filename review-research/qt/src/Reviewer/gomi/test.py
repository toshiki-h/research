
import sys
import csv
import MySQLdb
from collections import defaultdict

dic = defaultdict(lambda: 0)

### Read VotedReviewerList
hd = 0
AuthorId = 0
core = 0
for row in open(sys.argv[1], "r"): # voteReviewerList_all.csv
	if(hd == 0): # header
		hd = 1	
	else: # value
		words = row.strip().split(",")
		AuthorId = words[0]
		assert len(words) == 9
		assert len(words[0]) > 0 and len(words[8]) > 0
		core = words[8]
		dic[str(AuthorId)] = str(core)
		#print("%s:%s" % (AuthorId, dic[AuthorId]))

### Calcurate core or not core
hd = 0
AuthorId = 0
core = 0
for row in open(sys.argv[2], "r"):
	if(hd == 0): # header
		hd = 1
		print(str(row.strip())+",core")
	else: # value
		words = row.strip().split(",")
		AuthorId = words[1]
		core = dic[AuthorId]
		#print("%s:%s" % (AuthorId, dic[AuthorId]))
		print(str(row.strip())+","+str(core))
		



