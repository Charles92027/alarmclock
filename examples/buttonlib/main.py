import threading, atexit
from buttons import bigButton
from buttons import littleButton

import second

done = False

second.testThis()

def waitForDone():

	global done
	
	while done == False:
		pass
	




waitThread = threading.Thread(target = waitForDone)
waitThread.start()

def shutDown():

	global done
	global waitThread

	print("shutting down")

	done = True
	waitThread.join()

	GPIO.cleanup()

atexit.register(shutDown)
