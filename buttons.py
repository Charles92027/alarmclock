import time, RPi.GPIO as GPIO
from clock import clockFace

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class BigButton:

	bigButtonLedPin = 16
	bigButtonPin = 25

	def __init__(self):

		GPIO.setup(self.bigButtonLedPin, GPIO.OUT)
		GPIO.setup(self.bigButtonPin, GPIO.IN)

		GPIO.add_event_detect(self.bigButtonPin, GPIO.RISING, callback = self.pressed, bouncetime = 500)

		print("big button initialized")

	def light(self):
		GPIO.output(self.bigButtonLedPin, GPIO.HIGH)

	def unlight(self):
		GPIO.output(self.bigButtonLedPin, GPIO.LOW)

	def flash(self, count):
		for counter in range(count):
			self.light()
			time.sleep(.2)
			self.unlight()
			time.sleep(.2)
			
	def pressed(self, channel):
		
		if GPIO.input(channel) == GPIO.HIGH:
		
			print("big button pressed")
			
			import alarm
			alarm.alarm.bigButtonPressed();
			
			# send the button press signal to the alarm object
			
			#clockFace.chase()

			#while GPIO.input(channel) == GPIO.HIGH:
			#	pass

			#clockFace.time()

			#print("big button released")

			#self.flash(2)


class LittleButton:

	littleButtonPin = 26

	def __init__(self):

		GPIO.setup(self.littleButtonPin, GPIO.IN)
		GPIO.add_event_detect(self.littleButtonPin, GPIO.FALLING, callback = self.pressed, bouncetime = 500)
		
		print("little button initialized")

	def pressed(self, channel):
	
		if GPIO.input(channel) == GPIO.LOW:
			
			print("little button pressed")
			clockFace.address()
			
			while GPIO.input(channel) == GPIO.LOW:
				pass

			clockFace.time()
			print("little button released")

			global bigButton
			bigButton.flash(1)
		
bigButton = BigButton()
littleButton = LittleButton()

