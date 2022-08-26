from pygame import mixer
from threading import Thread
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
	playThread = None


	def __init__(self):
	
		mixer.init()
		self.setVolume(.5)		#initialize from config
		print("player initialized")
		
	def setVolume(self, volume):
		
		self.volume = volume
		mixer.music.set_volume(self.volume)

	def getVolume(self):
		return self.volume;

	def play(self, sound):
		
		self.stop()
		
		print("playing " + sound)
		mixer.music.load("sounds/" + sound)
		mixer.music.play()
		
		self.playThread = threading.Thread(target = self.whilePlaying)
		self.playThread.start()

	def stop(self):
		mixer.stop();
	
	def playng(self):
		return mixer.music.get_busy()
	
	def whilePlaying(self):
		while mixer.music.get_busy():
			pass

player = Player()