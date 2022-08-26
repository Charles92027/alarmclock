import board, time, threading, atexit
import RPi.GPIO as GPIO
import socket
from time import strftime
from buttons import bigButton
from buttons import littleButton
from adafruit_ht16k33.segments import BigSeg7x4
from flask import Flask

done = False
showTime = True

lights = [
	[0b00000001, 0b00000000, 0b00000000, 0b00000000],[0b00000000, 0b00000001, 0b00000000, 0b00000000],
	[0b00000000, 0b00000000, 0b00000001, 0b00000000],[0b00000000, 0b00000000, 0b00000000, 0b00000001],
	[0b00000000, 0b00000000, 0b00000000, 0b00000010],[0b00000000, 0b00000000, 0b00000000, 0b00000100],
	[0b00000000, 0b00000000, 0b00000000, 0b00001000],[0b00000000, 0b00000000, 0b00001000, 0b00000000],
	[0b00000000, 0b00001000, 0b00000000, 0b00000000],[0b00001000, 0b00000000, 0b00000000, 0b00000000],
	[0b00010000, 0b00000000, 0b00000000, 0b00000000],[0b00100000, 0b00000000, 0b00000000, 0b00000000]]

i2c = board.I2C()
display = BigSeg7x4(i2c, address=0x70)
display.brightness = 1.0

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)

#buttonLedPin = 16
#buttonPin = 25
#showIpPin = 26

#GPIO.setup(buttonLedPin, GPIO.OUT)
#GPIO.setup(buttonPin, GPIO.IN)
#GPIO.setup(showIpPin, GPIO.IN)

def displayTime():

	global showTime

	stringTime = "  " + strftime("%-I:%M")
	if (showTime == True):
		display.print(stringTime[-5:])

def timeLoop():
	
	global done
	
	while done == False:
		displayTime()
		time.sleep(.5)


#def lightButton():
#	GPIO.output(buttonLedPin, GPIO.HIGH)

#def unLightButton():
#	GPIO.output(buttonLedPin, GPIO.LOW)

#def flash(count):
#	for counter in range(count):
#		lightButton()
#		time.sleep(.2)
#		unLightButton()
#		time.sleep(.2)


#def buttonPressed(channel):
#	
#	global showTime
#	global lights
#	
#	if GPIO.input(channel) == GPIO.HIGH:
#
#		showTime = False
#		display.fill(0)
#		index = 0
#		
#		while GPIO.input(channel) == GPIO.HIGH:
#			#if mixer.music.get_busy() == False:
#			#	mixer.music.play()
#			display.set_digit_raw(0, lights[index][0])
#			display.set_digit_raw(1, lights[index][1])
#			display.set_digit_raw(2, lights[index][2])
#			display.set_digit_raw(3, lights[index][3])
#			time.sleep(.1)
#				
#			index = index + 1
#			if (index > 11):
#				index = 0
#
#		displayTime()
#		showTime = True
#		flash(3)

#def showIpSwitch(channel):
#
#	global showTime
#
#	if GPIO.input(channel) == GPIO.LOW:
#
#		showTime = False
#		display.fill(0)
#
#		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#		sock.settimeout(0)
#
#		try:
#			sock.connect(('10.254.254.254', 1))
#			ipAddress = sock.getsockname()[0]
#		except:
#			ipAddress = '127.0.0.1'
#		finally:
#			sock.close()
#
#		message = ipAddress.replace(".", "-") + "   "
#		while GPIO.input(channel) == GPIO.LOW:
#			display.marquee(message, 0.25, False)
#		
#		stringTime = "  " + strftime("%-I%M")
#		message = message + stringTime[-5:]
#		display.marquee(message, 0.25, False)
#		
#		displayTime()
#
#		showTime = True
#

#GPIO.add_event_detect(buttonPin, GPIO.RISING, callback = buttonPressed, bouncetime = 500)
#GPIO.add_event_detect(showIpPin, GPIO.FALLING, callback = showIpSwitch, bouncetime = 500)

clockThread = threading.Thread(target = timeLoop)
clockThread.start()

bigButton.flash(5)

def shutDown():

	global showTime
	global done
	global clockThread
	
	print("shutting down")

	showTime = False;
	done = True
	
	clockThread.join()
	display.fill(0)
	GPIO.cleanup()

atexit.register(shutDown)

app = Flask(__name__)
import website

