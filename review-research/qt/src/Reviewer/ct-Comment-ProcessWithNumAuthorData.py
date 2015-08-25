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
idList = []
for line in open(sys.argv[1], "r"):
    words = line.strip().split(",")
    idList.append(words[0])

i = 1
id2List = []
numList = []
for line in open(sys.argv[2]):
    if(i > 1):
        words = line.strip().split(",")
        id2List.append(words[0])
        numList.append(words[6])
    i = i + 1

for (i,j,k) in zip(idList, id2List,numList):
    print i+","+k
    assert i == j

assert len(id2List) == len(idList) and len(id2List) == 68113 and len(idList) == 68113
