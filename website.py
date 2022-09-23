import os
from flask import render_template
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

@app.route("/sounds/<sound>/play")
def playSound(sound):

	player.play(sound)
	return(sound)
