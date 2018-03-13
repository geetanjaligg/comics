# Thanks to Marcel Oehler for Comic strips

import urllib2
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

@sched.scheduled_job(trigger='interval', minutes=30)
def getcomic():

	if len(sys.argv) < 2 or sys.argv[1] == 'calvin': # default is calvin
		print 'inside'
		exist = True
		while exist:
			year = random.choice(range(1985,1995))
			month = random.choice(range(1,12))
			day = random.choice(range(1,31))

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
			print url

			try:
				exist = False
				res = urllib2.urlopen(url)
				output = open(os.path.join(APP_IMAGES, 'calvin.gif'), 'wb')
				output.write(res.read())
				output.close()
				webbrowser.open(os.path.join(APP_IMAGES, 'calvin.gif'))
			except Exception, error:
				print error
				pass
			break

	elif sys.argv[1] == 'xkcd':
		url = 'http://c.xkcd.com/random/comic/'
		try:
			page = urllib2.urlopen(url)
			soup = BeautifulSoup(page)
			img = soup.find('div',{'id':'comic'}).find('img')['src']
			res = urllib2.urlopen(img)
			output = open(os.path.join(APP_IMAGES, 'xkcd.png'), 'wb')
			output.write(res.read())
			output.close()
			webbrowser.open(os.path.join(APP_IMAGES, 'xkcd.png'))
		except Exception, error:
			print error
			pass

	elif sys.argv[1] == 'explosm':
		url = 'http://explosm.net/comics/random/'
		try:
			page = urllib2.urlopen(url)
			soup = BeautifulSoup(page)
			img = soup.find('div',{'id':'maincontent'}).findAll('img')[5]['src']
			print img
			res = urllib2.urlopen(img)
			output = open(os.path.join(APP_IMAGES, 'explosm.png'), 'wb')
			output.write(res.read())
			output.close()
			webbrowser.open(os.path.join(APP_IMAGES, 'explosm.png'))
		except Exception, error:
			print error
			pass

while True:
    time.sleep(10)
sched.shutdown()



