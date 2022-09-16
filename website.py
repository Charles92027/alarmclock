import os
from flask import render_template
from alarmclock import app
import sounds
from sounds import player
from database import database

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/sounds/")
def listSounds():
	return(sounds.listSounds())

@app.route("/sounds/<sound>/play")
def playSound(sound):

	player.play(sound)
	return(sound)

@app.route("/alarms/")
def listAlarms():

	response = database.listAlarms()
	return(response)

@app.route("/alarm/<id>")
def editAlarm(id):
	return render_template("alarm.html", id = id)

@app.route("/alarm/<id>", methods=['POST'])
def updateAlarm():

	pass
