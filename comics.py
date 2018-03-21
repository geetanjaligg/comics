# Thanks to Marcel Oehler for Comic strips

from __future__ import print_function
import urllib.request, urllib.error, urllib.parse
from datetime import datetime
import random
import webbrowser
import os
from apscheduler.schedulers.background import BackgroundScheduler as Scheduler
import time
import sys
from bs4 import BeautifulSoup

sched = Scheduler()
sched.start()

# __file__ refers to the current file 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_IMAGES = os.path.join(APP_ROOT, 'images')

PLATFORM=sys.platform
AVAILABLE_COMICS = ['calvin', 'xkcd', 'explosm']

@sched.scheduled_job(trigger='interval', minutes=30)
def getcomic():

	if len(sys.argv) < 2:
		choice = random.choice(AVAILABLE_COMICS)
	else:
		choice = sys.argv[1] 

	if choice == 'calvin': # default is calvin
		# print ('inside')
		exist = True
		while exist:
			year = random.choice(list(range(1985,1995)))
			month = random.choice(list(range(1,12)))
			day = random.choice(list(range(1,31)))

			try:
				datetime(year,month,day)
			except ValueError:
				try:
					datetime(year,month,day-1)
					day = day - 1
				except ValueError:
					try:
						datetime(year,month,day-2)
						day = day - 2
					except ValueError:
						day = day - 3

			#zfill to add 0 before a number for number less than 10

			url = 'http://marcel-oehler.marcellosendos.ch/comics/ch/' + str(year) + '/' + str(month).zfill(2) + '/' + str(year) + str(month).zfill(2) + str(day).zfill(2) + '.gif'
			print (url)

			try:
				exist = False
				image_path = os.path.join(APP_IMAGES, 'calvin.gif')
				res = urllib.request.urlopen(url)
				output = open(image_path, 'wb')
				output.write(res.read())
				output.close()
				if PLATFORM == 'darwin':
					image_path = 'file://' + os.path.abspath(image_path)
				webbrowser.open(image_path)
			except Exception as error:
				print (error)
				pass
			break

	elif choice == 'xkcd':
		url = 'http://c.xkcd.com/random/comic/'
		try:
			page = urllib.request.urlopen(url)
			soup = BeautifulSoup(page, "html.parser")
			img = 'http:' + soup.find('div',{'id':'comic'}).find('img')['src']
			res = urllib.request.urlopen(img)
			image_path = os.path.join(APP_IMAGES, 'xkcd.png')
			output = open(image_path, 'wb')
			output.write(res.read())
			output.close()
			if PLATFORM == 'darwin':
				image_path = 'file://' + os.path.abspath(image_path)
			webbrowser.open(image_path)
		except Exception as error:
			print (error)
			pass

	elif choice == 'explosm':
		url = 'http://explosm.net/comics/random/'
		try:
			page = urllib.request.urlopen(url)
			soup = BeautifulSoup(page, "html.parser")
			img = 'http:' + soup.find('img',{'id':'main-comic'})['src']
			print (img)
			res = urllib.request.urlopen(img)
			image_path = os.path.join(APP_IMAGES, 'explosm.png')
			output = open(image_path, 'wb')
			output.write(res.read())
			output.close()
			if PLATFORM == 'darwin':
				image_path = 'file://' + os.path.abspath(image_path)
			webbrowser.open(image_path)
		except Exception as error:
			print (error)
			pass

while True:
    time.sleep(10)
sched.shutdown()



