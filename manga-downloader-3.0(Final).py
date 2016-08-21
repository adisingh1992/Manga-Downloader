################################################################################################
########				LIBRARY'S USED					########
################################################################################################

from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from time import sleep
import requests
import os

################################################################################################

################################################################################################
########		FUNCTION TO CREATE PDF'S OF VOLUMES SCRAPED			########
################################################################################################

def createPdf():
	for volume in range(1, 43):
		command = "cd Manga/Volume-%d; convert $(ls *.jpg | sort -n) Volume-%d.pdf" %(volume, volume)
		os.system(command)
		os.system("cd Manga/Volume-%d; rm *.jpg" %(volume))		

################################################################################################

if os.path.exists('Manga') == False: #CHECKING IF THE DIRECTORY 'MANGA' EXISTS TO CONTAIN ALL THE VOLUMES
	os.mkdir('Manga')

chapter = 1 #CHAPTER VALUES

#LIST CONTAINING LAST CHAPTER VALUE OF EVERY VOLUME,
#THE COUNTER RESETS AT VOLUME 17 AS IT MARKS THE START OF A NEW SERIES - 'DRAGONBALL Z'
chapter_last = [0,11,24,36,48,60,71,84,96,108,120,132,144,156,168,180,194,10,22,34,46,58,70,82,94,106,119,131,143,155,167,179,191,202,214,226,238,251,265,278,291,308,325]

print "Scraping Initiated.."

for volume in range(1,43): #LOOP TO GENERATE THE VOLUME NUMBER
	if os.path.exists('Manga/Volume-%d'%volume) == False:
		os.mkdir('Manga/Volume-%d' %volume) #CREATING A NEW DIRECTORY FOR THE NEW VOLUME

	page_count = 0

	while chapter != chapter_last[volume] + 1: #LOOPING WHILE EVERY CHAPTER IN THE VOLUME IS SCRAPED
		url = "http://mangafox.me/manga/dragon_ball/v"+str('%02d')%volume+"/c"+str('%03d')%chapter+"/1.html"
		r = requests.get(url)
		raw_html = BeautifulSoup(r.text, 'html.parser')

		image_source_url = raw_html.find('img').get('src')

		while True:
			l = len(image_source_url) - 7
			image_source_url = image_source_url[0:l]
			image_source_url = image_source_url+str('%03d' %page_count)+".jpg"
			image_data = requests.get(image_source_url)
			i = Image.open(BytesIO(image_data.content))
			if image_data.status_code != requests.codes.ok or i.mode == 'P': #CHECKING IF THE DATA RETURNED IS VALID
				break
			page_count = page_count + 1
			i.save("Manga/Volume-%d/%d.jpg" %(volume, page_count), "JPEG")
		print "Dragon Ball Volume-%d, Chapter-%d Scraped Successfully..!!"%(volume, chapter) 
		chapter = chapter + 1
		sleep(5) #STOPPING TO CATCH BREATH..

	if chapter_last[volume] == 194: #RESETING THE CHAPTER COUNTER FOR THE START OF THE NEW SERIES
		chapter = 1

	sleep(10) #ALLOWING THE WEB-SERVER TO HEAL ;)

os.system('clear')
print "All Volume's Have Been Successfully Scraped..!!"

print "Do You Want To Create Volume-Pdf's Too: Y/N"
choice = raw_input(">>>")

if choice == 'y' or choice == 'Y':
	createPdf()

print "All Tasks Completed Successfully"
print "################################"
print "So Long, Until We Meet Again..!!"
