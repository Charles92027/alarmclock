import os
from flask import render_template
from flask import request
from flask import redirect
from alarmclock import app
import sounds
from sounds import player
import database
from datetime import datetime

@app.route("/")
def index():

	db = database.get_db_for_web()
	alarms = db.execute(
		"SELECT DISTINCT"
		" alarm.id, alarm.theTime, alarm.startDate, alarm.endDate, alarm.sound, alarm.enabled"
		" FROM alarm ORDER BY alarm.id;"
	).fetchall()

	return render_template("index.html", alarmList = alarms, soundList = sounds.listSounds())

@app.route("/alarm/<id>", methods=("GET", "POST"))
def editAlarm(id):

	if request.method == "POST":
	
		print("weekDays", request.form["weekDay"])
	
		alarmId = request.form["alarmId"]
		theTime = request.form["theTime"]
		startDate = request.form["startDate"]
		endDate = request.form["endDate"]
		sound = request.form["sound"]
		enabled = request.form.get("enabled", 0)
		db = database.get_db_for_web()
		db.execute(
			"UPDATE alarm SET theTime = ?, startDate = ?, endDate = ?, sound = ?, enabled = ? WHERE id = ?;",
			(theTime, startDate, endDate, sound, enabled, alarmId)
		)
		db.commit()
		return redirect("/")

	db = database.get_db_for_web()
	alarm = db.execute(
		"SELECT DISTINCT"
		" alarm.id, alarm.theTime, alarm.startDate, alarm.endDate, alarm.sound, alarm.enabled"
		" FROM alarm WHERE alarm.id = {};".format(id)
	).fetchone()

	weekDays = db.execute(
		"SELECT alarmId, theDay, checked FROM ("
		"SELECT weekDay.alarmId, weekDay.theDay, 'checked' checked"
		" FROM weekDay"
		" WHERE alarmid = {0}"
		" UNION SELECT blanks.alarmid, blanks.theDay, blanks.checked "
		"FROM ("
		" SELECT {0} alarmid, 0 theDay, '' checked "
		" UNION SELECT {0} alarmid, 1 theDay, '' checked "
		" UNION SELECT {0} alarmid, 2 theDay, '' checked "
		" UNION SELECT {0} alarmid, 3 theDay, '' checked "
		" UNION SELECT {0} alarmid, 4 theDay, '' checked "
		" UNION SELECT {0} alarmid, 5 theDay, '' checked "
		" UNION SELECT {0} alarmid, 6 theDay, '' checked "
		") blanks "
		" LEFT JOIN weekDay "
		" ON blanks.alarmId = weekDay.alarmId "
		" AND blanks.theDay = weekDay.theDay "
		" WHERE weekDay.id IS NULL "
		") weekDays"
		" ORDER BY theDay;".format(id)
	).fetchall()

	
	return render_template("alarm.html", alarm = alarm, weekDays=weekDays, soundList = sounds.listSounds())

@app.route("/alarm/new", methods=("GET", "POST"))
def newAlarm():

	if request.method == "POST":

		theTime = request.form["theTime"]
		startDate = request.form["startDate"]
		endDate = request.form["endDate"]
		sound = request.form["sound"]
		enabled = request.form.get("enabled", 0)
		db = database.get_db_for_web()
		db.execute(
			"INSERT INTO alarm (theTime, startDate, endDate, sound, enabled) VALUES (?, ?, ?, ?, ?);",
			(theTime, startDate, endDate, sound, enabled)
		)
		db.commit()
		return redirect("/")

	db = database.get_db_for_web()

	weekDays = db.execute(
		" SELECT 0 alarmid, 0 theDay, '' checked "
		" UNION SELECT 0 alarmid, 1 theDay, '' checked "
		" UNION SELECT 0 alarmid, 2 theDay, '' checked "
		" UNION SELECT 0 alarmid, 3 theDay, '' checked "
		" UNION SELECT 0 alarmid, 4 theDay, '' checked "
		" UNION SELECT 0 alarmid, 5 theDay, '' checked "
		" UNION SELECT 0 alarmid, 6 theDay, '' checked "
	).fetchall()

	alarm = {'id': 0}
	return render_template("alarm.html", alarm = alarm, weekDays=weekDays, soundList = sounds.listSounds())


@app.route("/sounds/<sound>/play")
def playSound(sound):

	player.play(sound)
	return(sound)


@app.template_filter('strftime')
def _filter_datetime(date, fmt=None):

	if not fmt:
		fmt = '%mmm %d, %yyyy'
	
	return date.strftime(fmt)

