import sqlite3

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

			CREATE IF NOT EXISTS TABLE alarm (
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

class Database:

	def __init__(self):
		connection = sqlite3.connect("alarmclock.db")

		# create the tables if they don't already exist
		cursor = connection.cursor()
		cursor.executescript(schema)
		cursor.close()

	def maintenance(self):
		pass
		
	def getNextAlarm(self):
		pass
