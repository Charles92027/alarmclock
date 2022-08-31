import sqlite3
from datetime import date
from datetime import timedelta

schema = """
			CREATE TABLE IF NOT EXISTS clock (
				id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				theTime TIME NOT NULL
			);
			CREATE UNIQUE INDEX IF NOT EXISTS ix_clock_theTime ON clock (theTime);

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
				alarmId INT NOT NULL REFERENCES alarm(id),
				sound TEXT NOT NULL
			);

			CREATE TABLE IF NOT EXISTS weekDay (
				id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				alarmId INT NOT NULL REFERENCES alarm(id),
				theDay INT NOT NULL
			);

			CREATE TABLE IF NOT EXISTS skip (
				id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				alarmId INT NOT NULL REFERENCES alarm(id),
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

# check for calendar data
cursor = connection.cursor()
sql = "SELECT MIN(thedate) minDate, MAX(theDate) maxDate FROM calendar;"
recordset = cursor.execute(sql)
minDate, maxDate = recordset.fetchone()
cursor.close()

today = date.today()
thisDayLastYear = addYears(today, -1)
lastDayOfNextYear = date(today.year + 1, 12, 31)

print(f"The lowest date is {lastYear!r}, the highestDate is {lastDayOfNextYear}")

if minDate is None:
	pass
	print("Calendar is empty")
	
else:
	print(f"The lowest date is {minDate!r}, the highestDate is {maxDate}")


# step one, delete everything prior to one year ago
# step two, insert starting with 




# insert calendar data
# cursor = connection.cursor()

# today = date.today()
# firstDayOfTheYear = date(today.year, 1, 1)
# lastDayOfNextYear = date(today.year + 1, 12, 31)

# theDate = firstDayOfTheYear
# aDay = timedelta(days = 1)

# while (theDate <= lastDayOfNextYear):
	
	# theDateS = theDate.strftime("%Y-%m-%d")
	# sql = "INSERT INTO calendar(theDate, theDay) SELECT '" + theDateS + "' theDate, STRFTIME('%w', '" + theDateS + "') theDay;"
	# print(sql)
	# cursor.execute(sql)
	# theDate = theDate + aDay

# connection.commit()
# cursor.close()

# retrieve some data
#cursor = connection.cursor()
#cursor.execute('SELECT id, theTime, startDate, endDate, disabled FROM alarm');

#for row in cursor:
#   print(row[0], row[1], row[2], row[3], row[4]);

#cursor.close()

connection.close()
