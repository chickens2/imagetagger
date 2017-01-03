import urllib
from urllib import FancyURLopener
from PIL import Image,ImageFont,ImageDraw
import cacher
import msvcrt
import json
import os
import sys
from pprint import pprint
import pyperclip

NUM_SELECTIONS_EACH_IMAGE=3
customTags={}
tagsByImage={}
imageByTags={}
#adds to a list in a dict
def ad(dict,key,element):
	alist=None
	if key in dict:
		alist=dict[key]
	else:
		alist=[]
		dict[key]=alist
	if element not in alist:
		alist.append(element)

def findBetween(s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
def loadData():
	global customTags
	customTags={}
	with open('imageTags.json', 'r') as f:
		customTags = json.load(f)
	loadData2()
def saveData():
	global customTags
	with open('dataTemp.json', 'w') as f:
		 json.dump(customTags, f)
	os.remove('imageTags.json')
	os.rename('dataTemp.json', 'imageTags.json')
	saveData2()
def loadData2():
	global tagsByImage
	global imageByTags
	tagsByImage={}
	imageByTags={}
	for file in os.listdir('tagAssignments'):
		with open('tagAssignments/'+file, 'r') as f:
			tagsByImage.update(json.load(f))
	for key,value in tagsByImage.iteritems():
		for item in value:
			ad(imageByTags,item,key)
	print 'loaded stuff:'
	#pprint(tagsByImage)
	#pprint(imageByTags)
def saveData2():
	global tagsByImage
	for key,taglist in tagsByImage.iteritems():
		with open('tagAssignments/'+key+'.json', 'w') as f:
			json.dump({key:taglist},f)
def oneInList(list1,list2):
	for element in list1:
		if element in list2:
			return element
	return None
selectedCount=0
totalSelectionsMade=0
def processDataRecursive(tag,image):
	global NUM_SELECTIONS_EACH_IMAGE
	global tagsByImage
	global selectedCount
	global totalSelectionsMade
	print 'trying to do tag:'+tag
	if tag not in customTags:
		'not in customtags: '+tag
		return
	parts=tag.split(':')
	#print 'parts:'
	#pprint(parts)
	mod=None
	actualTag=None
	if len(parts)==2:
		mod=parts[0]
		actualTag=parts[1]
	else:
		actualTag=tag
	#print 'mod:'+ str(mod)
	if mod=='category':
		for tag2 in customTags[tag]:
			if processDataRecursive(tag2,image)=='exit':
				return 'exit'
	else:
		#alreadyThere=False
		#print 'tagsbyimage:'
		#pprint(tagsByImage)
		print 'doing category selection for '+tag
		tag2=None
		if  image in tagsByImage:
			tag2=oneInList(customTags[tag],tagsByImage[image])
		if tag2 is None:
			print 'choose:\n['+"]        [".join(customTags[tag])+']\n\n\n'
			charused=msvcrt.getch()
			if charused=='x':
				saveData()
				sys.exit()
			tag2=customTags[tag][int(charused)-1]
			print '['+tag2+']'
			ad( imageByTags,tag2,image)
			ad(tagsByImage,image,tag2)
			totalSelectionsMade+=1
			selectedCount+=1
			if selectedCount>=NUM_SELECTIONS_EACH_IMAGE:
				selectedCount=0
				return 'exit'
		return processDataRecursive(tag2,image)
			
def processData(image):
	global selectedCount
	selectedCount=0
	print 'processing image: '+image
	pyperclip.copy(image)
	return processDataRecursive('category:top',image)
# class MyOpener(FancyURLopener):
	# version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
def getPageData(url):
	#'https://static1.e621.net/data/preview/80/40/8040bd505bfa5b00e6fe0518419a1107.jpg'
	filename= cacher.getUrlFile(url)
	file=open(filename,'r')
	contents=file.read()
	file.close()
	parts=contents.split('Date:')
	data=[]
	for part in parts:
		#print part[:150]+'\n\n\n\n'
		url=part
		if url.find('src=')>0:
			url=url[url.find('src=')+5:]
			#print url[:150]+'\n\n\n\n'
			url=url[:url.find('"')]
			if 'download-preview' not in url and '.png' not in url:
				if len(url)>0 and " " not in url:
					#print url+"^"
					title=part[part.find('title="')+7:]
					#print title.find('\c')
					title=title[:title.find('\r')]
					if len(title)>0 and '\n' not in title:
						#print title+"&^^^^^^^^^^^^^^^"
						data.append((cacher.getUrlFile(url),title))
	return data
# myopener = MyOpener()
# page=myopener.open('https://e621.net/post/popular_by_day?day=29&month=12&year=2016')
# print page.read()
loadData()
#print(customTags)

#sys.exit()


#print 'tagsbyimage:'
#pprint(tagsByImage)
#sys.exit()
daynum=31
data=getPageData('https://e621.net/post/popular_by_day?day='+str(daynum)+'&month=12&year=2016')
index=0
while (True):
	if index>=len(data):
		index=0
		daynum-=1
		data=getPageData('https://e621.net/post/popular_by_day?day='+str(daynum)+'&month=12&year=2016')
	#print 'filename: '+data[index][0]
	#print 'fnlastpart:'+data[index][0][-3:]
	if data[index][0][-3:]=='jpg':
		img=Image.open(data[index][0])
		try:
			img.save("temp.jpg","JPEG")
		except:
			print 'image save didnt work?'
		processData(data[index][0].replace('cachedData/',''))
	index+=1
	print 'tsm:'+str(totalSelectionsMade)+" "+str(totalSelectionsMade%(NUM_SELECTIONS_EACH_IMAGE))
	if totalSelectionsMade>0 and totalSelectionsMade%(5*NUM_SELECTIONS_EACH_IMAGE)==0:
		print 'do you want to save (y/n):'
		while True:
			charused=msvcrt.getch()
			if charused=='y':
				saveData()
				break
			if charused=='n':
				sys.exit()
saveData()
		#print url