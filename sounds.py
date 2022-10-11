from pygame import mixer
from threading import Thread
import os, threading
from database import database

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
		
		row = database.fetchOne("SELECT volume FROM configuration LIMIT 1;")
		newVolume = row[0]
		self.volume = newVolume
		self.setVolume(self.volume)
		
		print("player initialized")
		
	def setVolume(self, newVolume):
		
		self.volume = newVolume
		mixer.music.set_volume(self.volume)
		database.nonQuery("UPDATE configuration SET volume = {};".format(newVolume))

	def getVolume(self):
		return self.volume;

	def play(self, sound):
		
		self.stop()
		
		print("playing " + sound)
		mixer.music.load("sounds/" + sound)
		mixer.music.play()
		
		self.playThread = threading.Thread(target = self.whilePlaying)
		self.playThread.start()

	def playing(self):
		return mixer.music.get_busy()
	
	def stop(self):
		mixer.stop();
	
	def whilePlaying(self):
		while mixer.music.get_busy():
			pass

player = Player()