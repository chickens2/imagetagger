import iterate621
import os
from shutil import copyfile
import sys
from pprint import pprint
filelist = [ f for f in os.listdir("sortedImages")]
for f in filelist:
    os.remove('sortedImages/'+f)
allfilelists=[]
for arg in sys.argv[1:]:
	print arg
	tags=iterate621.imageByTags.keys()
	if arg in tags:
		allfilelists.append(set(iterate621.imageByTags[arg]))
allfiles=set.intersection(*allfilelists)
pprint(allfiles)
for file in allfiles:
	copyfile('cachedData/'+file,'sortedImages/'+file.replace('jpg','.jpg'))