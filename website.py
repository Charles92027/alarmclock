import os
from flask import render_template
from alarmclock import app

@app.route("/")
def index():
	return render_template("index.html")


@app.route("/sounds/")
def listSounds():
	sounds = []
	for file in os.listdir("sounds/"):
		if file.endswith(".mp3"):
			sounds.append(file)

	print(sounds)
	return(sounds)

@app.route("/sounds/<sound>/play/")
def playSound(sound):

	print("playing " + sound)
	mixer.music.load("sounds/" + sound)
	mixer.music.play()
	
	return(sound)
