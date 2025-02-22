#!/usr/bin/python3
##################
# Author:Toshiki Hirao
# CreatedOn: 2015/08/12
# Summary: count comment process
##################

### Import lib
import re
import sys
import csv
import time
import MySQLdb
from collections import defaultdict
from datetime import datetime

### main
i = 1
p = int(sys.argv[2])
n = int(sys.argv[3])
o = sys.argv[4]
me = 0
ab = 0
re = 0
allCt = 0

idList = []
assert len(sys.argv) == 5
assert p >= 0 and n >= 0
assert "-c" in sys.argv[4] or "-r" in sys.argv[4]

for line in open(sys.argv[1], "r"):
    words = line.strip().split(",")
    process = words[3:]

    if process.count("P") == p and process.count("N") == n:
        #print i
        idList.append(words[0])
        allCt = allCt + 1
        if ("Re" in process):
            re = re + 1         # Rewrite
            assert "Re" in process[-1:]
        else:
            if words[2] == "1": # Merged
                assert "M" in process[-1:]
                me = me + 1
            if words[2] == "0": # Abandoned
                assert "A" in process[-1:]
                ab = ab + 1
    i = i + 1
### Output
if "c" in o:
    print(""%d,%d,%d  " % (me, ab, re)),
    #print("All:%d\nM:%d\nA:%d\nRe:%d\n" % (allCt, me, ab, re))
if "-r" in o:
    print(idList)
print ""
