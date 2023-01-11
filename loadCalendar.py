import sqlite3, time
from datetime import datetime
from datetime import date
from datetime import timedelta

connection = sqlite3.connect("alarmclock.db")
cursor = connection.cursor()

today = date.today()
aYearAgo = today - timedelta(days = 365)
lastDay = date(2200, 12, 31)

theDate = aYearAgo
aDay = timedelta(days = 1)

while (theDate <= lastDay):
			
	theDateS = theDate.strftime("%Y-%m-%d")
	sql = "INSERT OR IGNORE INTO calendar(theDate, theDay) SELECT '" + theDateS + "' theDate, STRFTIME('%w', '" + theDateS + "') theDay;"
	cursor.execute(sql)
	theDate = theDate + aDay

	connection.commit()
	cursor.close()

connection.close()
