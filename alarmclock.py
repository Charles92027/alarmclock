import threading, atexit, time
import RPi.GPIO as GPIO
from clock import ClockState
from clock import clockFace
from buttons import bigButton
from buttons import littleButton
from flask import Flask

bigButton.flash(5)
clockFace.setState(ClockState.TIME)

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

	clockFace.setState(ClockState.DONE)
	
	done = True
	waitThread.join()

	GPIO.cleanup()

atexit.register(shutDown)

app = Flask(__name__)
import website

