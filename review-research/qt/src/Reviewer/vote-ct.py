#!/usr/bin/python3

###################
# calcurate negative, positive and normal vote by each voter in all data.
###################
### import lib
import sys
import csv
import MySQLdb
from collections import defaultdict

### hashtable about score
sAll = defaultdict(lambda: 0)	# Number of total score
sa = defaultdict(lambda: 0)		# Number of +2 
sb = defaultdict(lambda: 0)		# Number of +1
sc = defaultdict(lambda: 0)		# Number of 0
sd = defaultdict(lambda: 0)		# Number of -1
se = defaultdict(lambda: 0)		# Number of -2


# Judge the message is vote message or not.
# @message:message contents
# @author:message author
def JudgeVoteScore(message, author, sAll, sa, sb, sc, sd, se):
	if("Patch Set 1: Looks good to me, approved" in message):
		sAll[author] += 1
		sa[author] += 1
		return 2
	if("Patch Set 1: Looks good to me, but someone else must approve" in message):
		sAll[author] += 1
		sb[author] += 1
		return 1
	if("Patch Set 1: Looks good to me" in message):
		sAll[author] += 1
		sa[author] += 1
		return 2
	if("Patch Set 1: Works for me" in message):
		sAll[author] += 1
		sb[author] += 1
		return 1
	if("Patch Set 1: Verified" in message):
		sAll[author] += 1
		sb[author] += 1
		return 1
	if("Patch Set 1: No score" in message):
		sAll[author] += 1
		sc[author] += 1
		return 0
	if("Patch Set 1: I would prefer that you didnt submit this" in message or "Patch Set 1: I would prefer that you didn't submit this" in message):
		sAll[author] += 1
		sd[author] += 1
		return -1
	if("Patch Set 1: I would prefer that you didnt merge this" in message or "Patch Set 1: I would prefer that you didn't merge this" in message):
		sAll[author] += 1
		se[author] += 1
		return -2
	if("Patch Set 1: Do not submit" in message):
		sAll[author] += 1
		se[author] += 1
		return -2
	########## auto test ##########
	#if("Patch Set 1: Sanity review passed" in message): ## auto test
	#	sAll[author] += 1
	#	sb[author] += 1
	#	return 1
	#if("Patch Set 1: Sanity problems found" in message): ## auto test
	#	sAll[author] += 1
	#	sd[author] += 1
	#	return -1
	#if("Patch Set 1: Major sanity problems found" in message): ## auto test
	#	sAll[author] += 1
	#	se[author] += 1
	#	return -2
	###############################

	return -100

# Judge the author is Auto test machine or not
# @author:message author
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

### get ReviewId
ReviewId = []
i = 0
for row in open(sys.argv[1], "r"):
	if i > 0:
		words = row.split(",")
		ReviewId.append(words[1]);
	else:
		pass
	i += 1

#print("%s, %s, %s, %s, %s, %s" % (ReviewId[0], ReviewId[1], ReviewId[2], ReviewId[3], ReviewId[4], ReviewId[5]))
#print("%d" % len(ReviewId))

### Access into MySQLdb
cnct = MySQLdb.connect(db="qt",user="root", passwd="toshi1126")
cursor = cnct.cursor()
i = 0
for Id in ReviewId:
	cursor.execute("select ReviewId, Message, AuthorId from Comment where ReviewId = "+Id+" and Message like 'Patch Set 1%';")
	lines = cursor.fetchall()
	for line in lines:
		message = line[1].replace("\n", " ")
		author = line[2]
		#print(str(line[0]) + " "+message)
		s = JudgeVoteScore(message, author, sAll, sa, sb, sc, sd, se)
		#if(s != -100 and s == 2):
		#	print(str(s)+" : "+str(author))
		#print(line[1].replace("\n", ""))
		#if i == 0:
		#	print(line[1])
		#i += 1
	#print("%s : %d -> %d %d %d %d %d " % (Id, sAll[author], sa[author], sb[author], sc[author], sd[author], se[author]))
	#print(string)
	#words[1] = string.strip()
	#print(word)
#cursor.execute("select ReviewId, OwnerId, LastUpdatedOn, Status from Review where OwnerId = '"+owner_id+"' and LastUpdatedOn < '"+create_date+"' and Status = 'merged';")
#lines = cursor.fetchall()

print("AuthorId,\"+2\",\"+1\",\"0\",\"-1\",\"-2\",all,percentage")
for name, value in sAll.items():
	if(IsAutoTest(name) != 1):
		#print("%s : %d = %d + %d + %d + %d + %d " % (name, sAll[name], sa[name], sb[name], sc[name], sd[name], se[name]))
		print("%s,%d,%d,%d,%d,%d,%d,%f " % (name, sa[name], sb[name], sc[name], sd[name], se[name], sAll[name], (sd[name]+se[name]) / float(sAll[name])))
