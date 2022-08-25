from pygame import mixer
import os


volume = 0

def init():
	global volume
	
	volume = .5		#initialize from config
	
	mixer.init()
	mixer.music.set_volume(volume)

def setVolume(newVolume):
	global volume;
	volume = newVolume
	return volume;


def getVolume():
	global volume;
	return volume;

def listSounds():
	sounds = []
	for file in os.listdir("sounds/"):
		if file.endswith(".mp3"):
			sounds.append(file)

	print(sounds)
	return(sounds)


def play(sound):
	print("playing " + sound)
	mixer.music.load("sounds/" + sound)
	mixer.music.play()
	

def stop():
	mixer.stop();
	
def playng():
	return mixer.music.get_busy()
	
def whilePlaying():
	while mixer.music.get_busy():
		pass