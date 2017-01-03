import iterate621
import os
from shutil import copyfile
import sys
from pprint import pprint

filelist = [ f for f in os.listdir("sortedImages")]
for f in filelist:
    os.remove(f)
allfiles=[]
for arg in sys.argv[1:]:
	print arg
	tags=iterate621.imageByTags.keys()
	if arg in tags:
		allfiles.extend(iterate621.imageByTags[arg])
pprint(allfiles)
for file in allfiles:
	copyfile('cachedData/'+file,'sortedImages/'+file.replace('jpg','.jpg'))