from datetime import date
import time
from datetime import timedelta
import os

def addYears(theDate, years):

	newDate = theDate

	try:
		newDate = theDate.replace(year = theDate.year + years)

	except ValueError:
		newDate = theDate + (date(theDate.year + years, 1, 1) - date(theDate.year, 1, 1))
		
	return newDate

def getTimeZone():
	return open('/etc/timezone').read().strip()

def setTimeZone(newTimeZone):

	from database import database
	database.nonQuery("UPDATE configuration SET timeZone = '{}';".format(newTimeZone))
	
	command = "sudo timedatectl set-timezone {}".format(newTimeZone)
	os.system(command)
	
	time.tzset()


def getTimeZones():

	import os
	output = os.popen("cd /usr/share/zoneinfo/posix && find * -type f -or -type l | sort").read()
	timeZones = output.split('\n')
	return timeZones
	