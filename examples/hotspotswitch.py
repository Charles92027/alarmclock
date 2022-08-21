import RPi.GPIO as GPIO

hotspotPin = 26

def hotspotSwitch(channel):
	
	if GPIO.input(hotspotPin) == GPIO.HIGH:
		print("hotspotPin is high")
	else:
		print("hotspotPin is low")


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(hotspotPin, GPIO.IN)
GPIO.add_event_detect(hotspotPin, GPIO.BOTH, callback = hotspotSwitch, bouncetime = 500)

message = input("press enter to quit")

GPIO.cleanup()
