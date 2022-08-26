from pygame import mixer
import os, threading

def listSounds():
	sounds = []
	for file in os.listdir("sounds/"):
		if file.endswith(".mp3"):
			sounds.append(file)

	print(sounds)
	return(sounds)

class Player:

	volume = .5

	def __init__(self):
	
		mixer.init()
		self.setVolume(.5)		#initialize from config
		print("player initialized")
	
	def setVolume(self, volume):
		
		self.volume = volume
		mixer.music.set_volume(self.volume)

	def getVolume():
		return self.volume;

	def play(self, sound):
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

player = Player()