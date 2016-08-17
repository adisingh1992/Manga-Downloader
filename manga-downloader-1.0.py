##########################################################################
##			Dragon Ball Manga Downloader			##
##########################################################################

from PIL import Image
from io import BytesIO
from time import sleep
import requests
import os

prompt = ">>>"

##########################################################################
##Function To Create Volume-Pdf From Images				##
##########################################################################

def createPdf():
	command = "cd Manga; convert *.jpg Volume-%d/Chapter-%d.pdf" %(volume_number, chapter_number)
	os.system(command)

##########################################################################
##Function To Cleanup The Mess						##
##########################################################################

def cleanup():
	os.system('cd Manga; rm *.jpg')

##########################################################################
##Scraping The Manga							##
##########################################################################

if os.path.exists('Manga') == False:
	os.mkdir('Manga')

while True:
	os.system('clear')
	
	print "Enter Manga URL"
	url = raw_input(prompt)

	print "Enter Starting Page-Count"
	page_count = int(raw_input(prompt))

	print "Enter The Volume Number"
	volume_number = int(raw_input(prompt))
	print volume_number

	if os.path.exists('Manga/Volume-%d'%volume_number) == False:
		os.mkdir('Manga/Volume-%d')%volume_number	
	
	print "Enter The Chapter Number"
	chapter_number = int(raw_input(prompt))

	print "Scraping Initiated.."
	
	while True:
		url_c = url+str('%03d') %page_count+".jpg"
		r = requests.get(url_c)
		i = Image.open(BytesIO(r.content))
		if r.status_code != requests.codes.ok or i.mode == 'P':
			break
		i.save("Manga/%d.jpg"%page_count, "JPEG")
		page_count = page_count + 1
	createPdf()
	sleep(5)
	cleanup()

	print "Wanna Scrape Another Manga?? Y/N"
	choice = raw_input(prompt)
	if choice == 'N' or choice == 'n':
		break

print "Enjoy %d Pages Worth Of Action Your Favorite Manga..!!" %(page_count - 1)

##########################################################################
##########################################################################
