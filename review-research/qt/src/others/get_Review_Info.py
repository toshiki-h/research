##############################################
# file		: get_Review_Info.sh				 
# author	: toshiki hirao			 
# e-mail	: hirao.toshiki.ho7@is.naist.jp	 
# date		: 2015/06/11				
# upsate	: 2015/06/11	 
# summary	: 					 
##############################################

### Bug report ###
# $./get_Review_Info.py 
# bag:Not moving and I need to reboot
##################

### need to Fix code ###
# this code don't extract data sorted by 'WrittenOn'.
########################


### Import
import MySQLdb
import sys

### File Open 
f_patch_list = open(sys.argv[1], "r")
#f_csv = open(sys.argv[2], "w")

for Id in f_patch_list:
	if Id != "\n": 			## error process:when it is not patchId and is "\n")
		### Access MySQL
		connector = MySQLdb.connect(db="qt",user="root", passwd="toshi1126")
		cursor1 = connector.cursor()
		cursor2 = connector.cursor()
		
		### Select ReviewId and CreatedOn
		cursor1.execute("select ReviewId,CreatedOn from PatchSet where ReviewId = "+Id)
		rows1 = cursor1.fetchall()
		
		### Extract reviewId and CreatedOn
		i = 1
		set2_date = "0"
		for row1 in rows1:
			if i == 2:
				#review_id = str(row1[0])
				set2_date = str(row1[1])
			i += 1
		
		### Select messages before set2_WrittenOn
		if i > 2: 
			cursor2.execute("select ReviewId, AuthorId, WrittenOn, Message from Comment where ReviewId = "+Id+" and WrittenOn < '"+set2_date+"'")
			rows2 = cursor2.fetchall()

			### Write to f_csv file
			for row2 in rows2:
				sys.stdout.write(str(row2[0])+","+str(row2[1])+","+str(row2[2])+",")
				for clm in row2[3]:
					#print "'"+clm+"'",
					clm = clm.strip("\n")
					if len(clm) > 0:
						sys.stdout.write(clm)
				print ""
				#f_csv.write(str(row2[0])+","+str(row2[1])+","+str(row2[2])+","+str(row2[3]).strip("\n").strip("\r"))
				#print (str(row2[0])+","+str(row2[1])+","+str(row2[2])+","+str(row2[3])).strip("\n").strip("\r")
	
### Finalize
cursor1.close()
cursor2.close()
connector.close()
f_patch_list.close()
