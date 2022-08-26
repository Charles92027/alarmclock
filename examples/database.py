import sqlite3

schema = """CREATE TABLE IF NOT EXISTS alarm (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		theTime TIME NOT NULL,
		startDate DATE NOT NULL DEFAULT CURRENT_DATE,
		endDate DATE NULL,
		disabled BIT DEFAULT FALSE
	);

	CREATE TABLE IF NOT EXISTS weekDay (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		alarmId INTEGER NOT NULL REFERENCES alarm(id),
		weekDay INTEGER NOT NULL
	);

	CREATE TABLE IF NOT EXISTS skip (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		alarmId INTEGER NOT NULL REFERENCES alarm(id),
		theDate DATETIME NOT NULL
	);"""

print(schema);

connection = sqlite3.connect("alarms.db")

# create the tables if they don't already exist
cursor = connection.cursor()
cursor.executescript(schema)
cursor.close()

# insert some data
cursor = connection.cursor()
cursor.execute("INSERT INTO alarm(theTime, startDate) VALUES ('04:45', '2022-08-26');")
cursor.execute("INSERT INTO alarm(theTime, startDate) VALUES ('15:00', '2022-09-01');")
connection.commit()
cursor.close()

# retrieve some data
cursor = connection.cursor()
cursor.execute('SELECT id, theTime, startDate, endDate, disabled FROM alarm');

for row in cursor:
    print(row[0], row[1], row[2], row[3], row[4]);

cursor.close()


connection.close()
