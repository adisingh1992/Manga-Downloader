##########################################################################
##			Dragon Ball Manga Downloader			##
##########################################################################

from PIL import Image
from io import BytesIO
from time import sleep
import requests
import os

file = open('dbz_manga_urls.txt')
url_list = file.read().split()
volume_count = 0
total_page_count = 0

##########################################################################
##Function To Create Volume-Pdf From Images				##
##########################################################################

def createPdf():
	command = "cd Manga; convert *.jpg Volume-%d.pdf" %volume_count
	os.system(command)

##########################################################################
##Function To Cleanup The Mess						##
##########################################################################

def cleanup():
	os.system('cd Manga; rm *.jpg')

##########################################################################
##Scraping The Manga							##
##########################################################################

if os.path.exists == False:
	os.mkdir('Manga')

print "Scraping Initiated.."

for url in url_list:
	volume_count = volume_count + 1
	page_count = 0
	while True:
		url_c = url+str('%03d') %page_count+".jpg"
		r = requests.get(url_c)
		i = Image.open(BytesIO(r.content))

		if r.status_code != requests.codes.ok or i.mode == 'P':
			break

		i.save("Manga/%d.jpg"%page_count, "JPEG")

		page_count = page_count + 1
		total_page_count = total_page_count + 1
	createPdf()
	sleep(10)
	cleanup()
	print "Volume %d Scraped Successfully..!!" %volume_count
file.close()
print "Enjoy %d Pages Worth Of Action In %d Volumes Of Your Favorite Manga..!!" %(total_page_count,volume_count)

##########################################################################
##########################################################################
