import time, RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

bigButtonLedPin = 16
bigButtonPin = 25

GPIO.setup(bigButtonLedPin, GPIO.OUT)
GPIO.setup(bigButtonPin, GPIO.IN)


def lightButton():
	GPIO.output(bigButtonLedPin, GPIO.HIGH)

def unLightButton():
	GPIO.output(bigButtonLedPin, GPIO.LOW)

def flash(count):
	for counter in range(count):
		lightButton()
		time.sleep(.2)
		unLightButton()
		time.sleep(.2)
			
def pressed(channel):
	
	if GPIO.input(channel) == GPIO.HIGH:
	
		print("big button pressed")
	
		while GPIO.input(channel) == GPIO.HIGH:
			flash(1)

		print("big button released")

		flash(4)



GPIO.add_event_detect(bigButtonPin, GPIO.RISING, callback = pressed, bouncetime = 500)

flash(5)
print("big button initialized")
message = input("press enter to quit")

GPIO.cleanup()