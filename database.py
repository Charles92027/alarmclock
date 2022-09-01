import sqlite3
import util
from datetime import date
from datetime import timedelta

class Database:

	def __init__(self):
		self.createSchema()
		self.maintenance()

	def createSchema(self):

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
						sound TEXT NOT NULL,
						disabled BIT DEFAULT FALSE
					);
					CREATE INDEX IF NOT EXISTS ix_alarm_startDate ON alarm (startDate);
					CREATE INDEX IF NOT EXISTS ix_alarm_endDate ON alarm (endDate);

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
	
		connection = sqlite3.connect("alarmclock.db")

		# create the tables
		cursor = connection.cursor()
		cursor.executescript(schema)
		cursor.close()
		
		connection.close()
		
	def maintenance(self):
	
		connection = sqlite3.connect("alarmclock.db")
		cursor = connection.cursor()

		# remove records older than a year
		sql = "DELETE FROM CALENDAR WHERE theDate < DATE('NOW', 'LOCALTIME', '-1 YEAR')"
		cursor.execute(sql)
		sql = "DELETE FROM alarm WHERE endDate < DATE('NOW', 'LOCALTIME', '-1 YEAR')"
		cursor.execute(sql)

		today = date.today()
		thisDayLastYear = util.addYears(today, -1)
		lastDayOfNextYear = date(today.year + 1, 12, 31)
		aDay = timedelta(days = 1)

		theDate = thisDayLastYear
		aDay = timedelta(days = 1)

		# insert calendar records to contain a list of dates from 1 year ago today to the last day of next year
		while (theDate <= lastDayOfNextYear):
			
			theDateS = theDate.strftime("%Y-%m-%d")
			sql = "INSERT OR IGNORE INTO calendar(theDate, theDay) SELECT '" + theDateS + "' theDate, STRFTIME('%w', '" + theDateS + "') theDay;"
			cursor.execute(sql)
			theDate = theDate + aDay

		connection.commit()
		cursor.close()

		connection.close()
		
	def getNextAlarm(self):
	
		sql = """
			SELECT x.id, x.theDate, x.theTime, x.theDateTime, x.sound FROM (
				SELECT
					alarm.id,
					calendar.theDate,
					alarm.theTime,
					DATETIME(calendar.theDate, alarm.theTime) theDateTime,
					alarm.sound
				FROM alarm
					JOIN weekDay
						ON alarm.id = weekDay.alarmId
					JOIN calendar
						ON alarm.startDate <= calendar.theDate
						AND alarm.endDate >= calendar.theDate
						AND calendar.theDate >= DATE('NOW', 'LOCALTIME')
						AND calendar.theDate <= DATE('NOW', 'LOCALTIME', '+1 DAY')
						AND weekDay.theDay = calendar.theDay
				WHERE alarm.disabled = FALSE
				UNION
				SELECT
					alarm.id,
					calendar.theDate,
					alarm.theTime,
					DATETIME(calendar.theDate, alarm.theTime) theDateTime,
					alarm.sound
				FROM alarm
					LEFT JOIN weekDay
						ON alarm.id = weekDay.alarmId
					JOIN calendar
						ON alarm.startDate <= calendar.theDate
						AND alarm.endDate >= calendar.theDate
						AND calendar.theDate >= DATE('NOW', 'LOCALTIME')
						AND calendar.theDate <= DATE('NOW', 'LOCALTIME', '+1 DAY')
				WHERE alarm.disabled = FALSE
				AND weekDay.ID IS NULL

			) AS x
				LEFT JOIN skip
					ON x.id = skip.alarmId
					AND x.theDate = skip.theDate
			WHERE skip.id IS NULL
			AND x.theDateTime >= DATETIME('NOW', 'LOCALTIME')
			ORDER BY x.theDateTime
			LIMIT 1;
			"""

		connection = sqlite3.connect("alarmclock.db")

		cursor = connection.cursor()
		cursor.execute(sql)
		recordset = cursor.fetchone()
		cursor.close()

		connection.close()

		return recordset



database = Database()