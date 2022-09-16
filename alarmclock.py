import threading, atexit, time
import RPi.GPIO as GPIO
from clock import clockFace
from buttons import bigButton
from buttons import littleButton
from flask import Flask
from database import database
from alarm import alarm

#bigButton.flash(5)
#clockFace.address()
#time.sleep(.5)
clockFace.time()

done = False

def waitLoop():
	global done
	while done == False:
		time.sleep(.5)

waitThread = threading.Thread(target = waitLoop)
waitThread.start()

def shutDown():

	global done
	global waitThread
	
	print("shutting down")

	clockFace.done()
	
	done = True
	waitThread.join()

	GPIO.cleanup()

atexit.register(shutDown)

app = Flask(__name__)
import website

