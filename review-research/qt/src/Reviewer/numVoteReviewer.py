#!/usr/bin/python3

### import lib
import sys
import csv
import MySQLdb
from collections import defaultdict

# JudgeVoteScore: Judge that the message is vote message or not
# @message:message contents
# @author:message author
def JudgeVoteScoreInPatchSetId_1(message):
	if("Patch Set 1: Looks good to me, approved" in message):
		return 2
	if("Patch Set 1: Looks good to me, but someone else must approve" in message):
		return 1
	if("Patch Set 1: Looks good to me" in message):
		return 2
	if("Patch Set 1: Works for me" in message):
		return 1
	if("Patch Set 1: Verified" in message):
		return 1
	if("Patch Set 1: No score" in message):
		return 0
	if("Patch Set 1: I would prefer that you didnt submit this" in message or "Patch Set 1: I would prefer that you didn't submit this" in message):
		return -1
	if("Patch Set 1: I would prefer that you didnt merge this" in message or "Patch Set 1: I would prefer that you didn't merge this" in message):
		return -2
	if("Patch Set 1: Do not submit" in message):
		return -2
	########## auto test ##########
	#if("Patch Set 1: Sanity review passed" in message): ## auto test
	#	return 1
	#if("Patch Set 1: Sanity problems found" in message): ## auto test
	#	return -1
	#if("Patch Set 1: Major sanity problems found" in message): ## auto test
	#	return -2
	###############################

	return -100	#This message is not vote message.

### Access into MySQLdb
cnct = MySQLdb.connect(db="qt",user="root", passwd="toshi1126")
cursor = cnct.cursor()

### Count vote reviewer 
i = 0
for row in open(sys.argv[1], "r"):
	if(i == 0):
		pass
	else:
		clms = row.split(",")
		#print(clms[1])
		ReviewId = clms[1]
		## Access MySQLdb
		cursor.execute("select ReviewId, PatchSetId, CreatedOn from PatchSet where ReviewId = '"+ReviewId+"' and PatchSetId = '0';")
		p_info = cursor.fetchall()
		Create_time = p_info[2]
 		cursor.execute("select ReviewId, Message, AuthorId from Comment where ReviewId = '"+Id+"' and Message like 'Patch Set 1%';")
		lines = cursor.fetchall()

		score = defaultdict(lambda: 0)
		vote_reviewer = []
		for line in lines:
			message = line[1].replace("\n", " ")
			author = line[2]
			if(author in vote_reviewer):
				vote_reviewer.append(author)
 			score[ReviewId] += JudgeVoteScoreInPatchSetId_1(message)
		print("%s %d %d" % (ReviewId, len(vote_reviewer), score[ReviewId]))
	i += 1
