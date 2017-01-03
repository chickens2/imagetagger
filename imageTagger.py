import iterate621
import msvcrt
import sys
from PIL import Image,ImageFont,ImageDraw
daynum=31
data=iterate621.getPageData('https://e621.net/post/popular_by_day?day='+str(daynum)+'&month=12&year=2016')
index=0
while (True):
	if index>=len(data):
		index=0
		daynum-=1
		data=iterate621.getPageData('https://e621.net/post/popular_by_day?day='+str(daynum)+'&month=12&year=2016')
	#print 'filename: '+data[index][0]
	#print 'fnlastpart:'+data[index][0][-3:]
	if data[index][0][-3:]=='jpg':
		img=Image.open(data[index][0])
		try:
			img.save("temp.jpg","JPEG")
		except:
			print 'image save didnt work?'
		iterate621.processData(data[index][0].replace('cachedData/',''))
	index+=1
	print 'tsm:'+str(iterate621.totalSelectionsMade)+" "+str(iterate621.totalSelectionsMade%(iterate621.NUM_SELECTIONS_EACH_IMAGE))
	if iterate621.totalSelectionsMade>0 and iterate621.totalSelectionsMade%(5*iterate621.NUM_SELECTIONS_EACH_IMAGE)==0:
		print 'do you want to save (y/n):'
		while True:
			charused=msvcrt.getch()
			if charused=='y':
				iterate621.saveData()
				break
			if charused=='n':
				sys.exit()
iterate621.saveData()