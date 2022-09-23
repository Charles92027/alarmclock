import sqlite3
import util
import datetime
from datetime import date
from datetime import timedelta

from flask import current_app
from flask import g


def get_db_for_web():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            "alarmclock.db", detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


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
						enabled BIT DEFAULT TRUE
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
				WHERE alarm.enabled = TRUE
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
				WHERE alarm.enabled = TRUE
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

	def listAlarms(self):
	
		sql = """
			SELECT DISTINCT
				alarm.id,
				alarm.theTime,
				alarm.startDate,
				alarm.endDate,
				alarm.sound,
				alarm.enabled
			FROM alarm
			ORDER BY alarm.id;
		"""

		connection = sqlite3.connect("alarmclock.db")

		cursor = connection.cursor()
		recordset = cursor.execute(sql)
		
		jsonResult = "["
		jsonElement = ""
		comma = ""
		oldId = 0
		
		row = recordset.fetchone()
		while row != None:
		
			id, theTime, startDate, endDate, sound, enabled = row
			
			#theTime = datetime.strptime(theTime).strftime("%-I:%M")

			#if startDate == endDate:
			#	endDate = datetime.strptime(endDate).strftime("%m/%d/%Y")
			#else:
			#	endDate = ""

			#startDate = datetime.strptime(startDate).strftime("%m/%d/%Y")
			
			jsonElement = '{{"id":"{}","theTime":"{}","startDate":"{}","endDate":"{}","sound":"{}","enabled":"{}"}}'.format(id, theTime, startDate, endDate, sound, enabled)
			jsonResult = jsonResult + comma + jsonElement
			comma = ","
			
			row = recordset.fetchone()
		
		cursor.close()

		connection.close()

		jsonResult += "]"

		print(jsonResult)

		return jsonResult	
	
	def getAlarm(id):
		sql = """
			SELECT DISTINCT
				alarm.id,
				alarm.theTime,
				alarm.startDate,
				alarm.endDate,
				alarm.sound,
				alarm.enabled
			FROM alarm
			WHERE alarm.id={};
		""".format(id);

		connection = sqlite3.connect("alarmclock.db")

		cursor = connection.cursor()
		row = cursor.execute(sql).fetchone()
		
		jsonElement = '{{"id":"{}","theTime":"{}","startDate":"{}","endDate":"{}","sound":"{}","enabled":"{}"}}'.format(row[0], row[1], row[2], row[3], row[4], row[5])

		cursor.close()
		connection.close()

		print(jsonResult)

		return jsonResult	
	

database = Database()