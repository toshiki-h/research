#!/usr/bin/python3

###################
# calcurate negative, positive and normal vote by each voter from PatchSetId-0 to PatchSetId-1.
###################

### import lib
import sys
import csv
import MySQLdb
from collections import defaultdict

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

	return 999

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
re_wr = defaultdict(lambda: 0)

i = 0
Id_list = []
for row in open(sys.argv[1], "r"):
	if i > 0:
		words = row.split(",")
		Id_list.append(words[0])
		#re_wr[words[1]] = words[4]
		#print(words[1] + ":" + re_wr[words[1]])
	else:
		pass
	i += 1

### Access into MySQLdb
cnct = MySQLdb.connect(db="qt",user="root", passwd="toshi1126")
cursor = cnct.cursor()
time_csr = cnct.cursor()

i = 0
for Id in Id_list:
	#print(Id)
	### hashtable about score
	sAll = defaultdict(lambda: 0)	# Number of total score
	sa = defaultdict(lambda: 0)		# Number of +2 
	sb = defaultdict(lambda: 0)		# Number of +1
	sc = defaultdict(lambda: 0)		# Number of 0
	sd = defaultdict(lambda: 0)		# Number of -1
	se = defaultdict(lambda: 0)		# Number of -2
	com_num = 0
	pos = 0
	nor = 0
	neg = 0
	aut = []
	#print(i)

	#--time_csr.execute("select CreatedOn from PatchSet where ReviewId = '"+Id+"' and PatchSetId = '0';")
	#--creOn = time_csr.fetchall()
	#--for c in creOn:
	#--	time = c[0]
	#--print(time)
	cursor.execute("select ReviewId, Message, AuthorId from Comment where ReviewId = '"+Id+"';")
	lines = cursor.fetchall()
	#--cursor.execute("select ReviewId, Message, AuthorId from Comment where WrittenOn <= '"+str(time)+"';")
	#--lines = cursor.fetchall()
	for line in lines:
		message = line[1].replace("\n", " ")
		author = line[2]
		#if i == 0:
			#print(i)
			#print(str(author)+" "+message)
		if(IsAutoTest(author) != 1):
			if(JudgeVoteScore(message, author, sAll, sa, sb, sc, sd, se) > 0 and JudgeVoteScore(message, author, sAll, sa, sb, sc, sd, se) < 3):
				pos += 1
				if(author in aut):
					pass
				else:
					aut.append(author)
			if(JudgeVoteScore(message, author, sAll, sa, sb, sc, sd, se) == 0):
				nor += 1
				if(author in aut):
					pass
				else:
					aut.append(author)
			if(JudgeVoteScore(message, author, sAll, sa, sb, sc, sd, se) < 0):
				neg += 1
				if(author in aut):
					pass
				else:
					aut.append(author)
			if("Patch Set 1:" in message):
				com_num += 1
	if (pos+nor+neg) != 0:
		#print(Id)
		#print("%d,%d,%d,%d,%f,%f,%f,%d" % (pos, nor, neg, (pos+nor+neg), float(neg)/(pos+nor+neg), float(nor)/(pos+nor+neg),float(pos)/(pos+nor+neg), com_num))
		#print(str(len(aut))+","+str(float(neg)/(pos+nor+neg)))
		print("%d,%d,%d,%d,%f,%f,%f,%d" % (len(aut), pos, nor, neg, float(pos)/(pos+nor+neg), float(nor)/(pos+nor+neg),float(neg)/(pos+nor+neg), com_num))
	else:
		#print(Id)
		#print("%d,%d,%d,%d,%f,%f,%f,%d" % (pos, nor, neg, (pos+nor+neg), 0, 0, 0,com_num))
		#print(str(len(aut))+","+str(float(0)))
		print("%d,%d,%d,%d,%f,%f,%f,%d" % (len(aut), pos, nor, neg, 0, 0, 0, com_num))
	#print(Id)
	i += 1
