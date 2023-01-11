import sqlite3, threading, time
import util
from datetime import datetime
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

	done = False
	maintenanceThread = None

	def __init__(self):
		# self.createSchema()

		self.maintenanceThread = threading.Thread(target = self.maintenance)
		self.maintenanceThread.start()

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
						theDate DATE NOT NULL
					);
					
					CREATE TABLE IF NOT EXISTS configuration (
						id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
						timeZone TEXT NOT NULL,
						volume REAL NOT NULL DEFAULT .5,
						brightness REAL NOT NULL DEFAULT 1
					);
					
					INSERT INTO configuration(timeZone, volume, brightness) 
					SELECT 'America/Los_Angeles', .5, 1
					WHERE NOT EXISTS(SELECT 1 FROM configuration);
				"""	
	
		connection = sqlite3.connect("alarmclock.db")

		# create the tables
		cursor = connection.cursor()
		cursor.executescript(schema)
		
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

	
	def stopMaintenance(self):
		self.done = True
		self.maintenanceThread.join()
	
	def maintenance(self):
	
		lastMaintenanceRun = datetime.now() - timedelta(hours = 48)

		while self.done == False:

			interval = (datetime.now() - lastMaintenanceRun)

			mm = interval.total_seconds() / 60
			if mm > 2880:
			
				connection = sqlite3.connect("alarmclock.db")
				cursor = connection.cursor()

				# remove records older than a year
				sql = "DELETE FROM calendar WHERE theDate < DATE('NOW', 'LOCALTIME', '-1 YEAR')"
				cursor.execute(sql)
				sql = "DELETE FROM alarm WHERE endDate < DATE('NOW', 'LOCALTIME', '-1 YEAR')"
				cursor.execute(sql)

				# remove skip records older than three days
				sql = "DELETE FROM skip WHERE theDate < DATE('NOW', 'LOCALTIME', '-3 DAY')"
				cursor.execute(sql)

				connection.commit()
				cursor.close()

				connection.close()
				
				lastMaintenanceRun = datetime.now()
			
			time.sleep(1)

		
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
						AND calendar.theDate <= DATE('NOW', 'LOCALTIME', '+7 DAY')
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
						AND calendar.theDate <= DATE('NOW', 'LOCALTIME', '+7 DAY')
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
	
	def skipAlarmToday(self, alarmId):
		self.skipAlarm(alarmId, datetime.today())

	def skipAlarm(self, alarmId, theDate):

		sql = "INSERT INTO skip (alarmId, theDate) VALUES ({}, '{}')".format(alarmId, theDate.strftime("%Y-%m-%d"));	
		self.nonQuery(sql);
		
	def fetchOne(self, sql):
		db = sqlite3.connect("alarmclock.db", detect_types=sqlite3.PARSE_DECLTYPES)
		db.row_factory = sqlite3.Row
		row = db.execute(sql).fetchone()
		return row

	def nonQuery(self, sql):
		db = sqlite3.connect("alarmclock.db", detect_types=sqlite3.PARSE_DECLTYPES)
		db.row_factory = sqlite3.Row
		db.execute(sql)
		db.commit();
	

database = Database()
