# Thanks to Marcel Oehler for Comic strips

import urllib2
from datetime import datetime
import random
import webbrowser
import os
from apscheduler.scheduler import Scheduler
import time

sched = Scheduler()
sched.start()

# __file__ refers to the current file 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_IMAGES = os.path.join(APP_ROOT, 'images')

@sched.interval_schedule(minutes=1)
def getcomic():
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


while True:
    time.sleep(10)
sched.shutdown()



