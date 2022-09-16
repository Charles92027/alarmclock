import sqlite3
from datetime import date
from datetime import timedelta

schema = """
			CREATE TABLE IF NOT EXISTS calendar (
				id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				theDate DATE NOT NULL,
				theDay INT NOT NULL
			);
			CREATE UNIQUE INDEX IF NOT EXISTS ix_calendar ON calendar (theDate);

			CREATE TABLE IF NOT EXISTS alarm (
				id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				theTime TIME NOT NULL,
				startDate DATE NOT NULL DEFAULT CURRENT_DATE,
				endDate DATE NOT NULL,
				disabled BIT DEFAULT FALSE
			);
			CREATE INDEX IF NOT EXISTS ix_alarm_startDate ON alarm (startDate);
			CREATE INDEX IF NOT EXISTS ix_alarm_endDate ON alarm (endDate);

			CREATE TABLE IF NOT EXISTS alarmSound (
				id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				alarmId INT NOT NULL REFERENCES alarm(id) ON DELETE CASCADE,
				sound TEXT NOT NULL
			);

			CREATE TABLE IF NOT EXISTS weekDay (
				id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				alarmId INT NOT NULL REFERENCES alarm(id) ON DELETE CASCADE,
				theDay INT NOT NULL
			);

			CREATE TABLE IF NOT EXISTS skip (
				id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				alarmId INT NOT NULL REFERENCES alarm(id) ON DELETE CASCADE,
				theDate DATETIME NOT NULL
			);
		"""

#print(schema);

connection = sqlite3.connect("alarmclock.db")

# create the tables
cursor = connection.cursor()
cursor.executescript(schema)
cursor.close()

def addYears(d, years):

	newDate = d

	try:
		newDate = d.replace(year = d.year + years)

	except ValueError:
		newDate = d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))
		
	return newDate

cursor = connection.cursor()

# remove records older than a year
sql = "DELETE FROM CALENDAR WHERE theDate < DATE('NOW', 'LOCALTIME', '-1 YEAR')"
cursor.execute(sql)
sql = "DELETE FROM alarm WHERE endDate < DATE('NOW', 'LOCALTIME', '-1 YEAR')"
cursor.execute(sql)

today = date.today()
thisDayLastYear = addYears(today, -1)
lastDayOfNextYear = date(today.year + 1, 12, 31)
aDay = timedelta(days = 1)

theDate = thisDayLastYear
aDay = timedelta(days = 1)

# insert calendar records to contain a list of dates from 1 year ago today to the last day of next year
while (theDate <= lastDayOfNextYear):
	
	theDateS = theDate.strftime("%Y-%m-%d")
	sql = "INSERT OR IGNORE INTO calendar(theDate, theDay) SELECT '" + theDateS + "' theDate, STRFTIME('%w', '" + theDateS + "') theDay;"
	cursor.execute(sql)
	
	######## This is super important
	last_row_id = cursor.lastrowid
	
	
	theDate = theDate + aDay

connection.commit()
cursor.close()


# check for calendar data
cursor = connection.cursor()
sql = "SELECT MIN(thedate) minDate, MAX(theDate) maxDate FROM calendar;"
recordset = cursor.execute(sql)
minDate, maxDate = recordset.fetchone()
cursor.close()

print(f"The lowest date is {minDate!r}, the highestDate is {maxDate}")


cursor = connection.cursor()
sql = "SELECT id, theDate, theDay FROM calendar LIMIT 10;"
recordset = cursor.execute(sql)

row = recordset.fetchone()

while row != None:
	id, theDate, theDay = row
	print(f"{id}, {theDate}, {theDay}")
	row = recordset.fetchone()

cursor.close()

connection.close()
