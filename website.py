import os
from flask import render_template
from flask import request
from flask import redirect
from alarmclock import app
import sounds
from sounds import player
import database

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

	return render_template("alarm.html", alarm = alarm, soundList = sounds.listSounds())

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

	alarm = {'id': 0}
	return render_template("alarm.html", alarm = alarm, soundList = sounds.listSounds())


@app.route("/sounds/<sound>/play")
def playSound(sound):

	player.play(sound)
	return(sound)
