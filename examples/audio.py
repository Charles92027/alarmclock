from pygame import mixer

mixer.init()
mixer.music.load("../sounds/snare.mp3")
mixer.music.set_volume(1.0)

try :
	#mixer.music.play(loops = -1)	# play forever
	mixer.music.play()
	while mixer.music.get_busy() == True:
		pass

except KeyboardInterrupt:
	# if user hits Ctrl/C then exit
	# (works only in console mode)
	mixer.music.fadeout(1000)
	mixer.music.stop()
	raise SystemExit

