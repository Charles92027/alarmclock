import os
from flask import render_template
from alarmclock import app
import sounds

@app.route("/")
def index():
	return render_template("index.html")


@app.route("/sounds/")
def listSounds():
	return(sounds.listSounds())

@app.route("/sounds/<sound>/play")
def playSound(sound):

	sounds.play(sound)
	return(sound)
