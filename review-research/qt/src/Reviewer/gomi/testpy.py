import re
pattern = re.compile(r'Patch Set [0-9]+: Abandoned')

pattern2 = re.compile(r'Change has been successfully cherry-picked as')
for line in open("test.txt", "r"):
	if(pattern.match(line)):
		print line.strip()
	if(pattern2.match(line)):
		print line.strip()

