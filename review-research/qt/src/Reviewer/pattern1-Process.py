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
assert len(sys.argv) == 3
m1 = sys.argv[2]

idList = []
me = 0
ab = 0
re = 0
allCt = 0
ct = 0

for line in open(sys.argv[1], "r"):
    words = line.strip().split(",")
    process = words[3:]
    if(m1 in process[0] and len(process) == 2):
        print words
        ct = ct + 1
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

print("%d %d %d %d" % (ct, me, ab, re))
