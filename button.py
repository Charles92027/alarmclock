import RPi.GPIO as GPIO

class BigButton:

	buttonLedPin = 16
	buttonPin = 25

	def __init__():

		GPIO.setup(buttonLedPin, GPIO.OUT)
		GPIO.setup(buttonPin, GPIO.IN)

		GPIO.add_event_detect(buttonPin, GPIO.RISING, callback = pressed, bouncetime = 500)

		flash(5)

	def lightButton():
		GPIO.output(buttonLedPin, GPIO.HIGH)

	def unLightButton():
		GPIO.output(buttonLedPin, GPIO.LOW)

	def flash(count):
		for counter in range(count):
			lightButton()
			time.sleep(.2)
			unLightButton()
			time.sleep(.2)
			
	def pressed(channel):
		
		if GPIO.input(channel) == GPIO.HIGH:
			while GPIO.input(channel) == GPIO.HIGH:
				# while pressed display chasing lights
				pass

			flash(3)


class IpButton:

	ipPin = 26

	def __init__():

		GPIO.setup(ipPin, GPIO.IN)
		GPIO.add_event_detect(ipPin, GPIO.FALLING, callback = pressed, bouncetime = 500)

	def pressed(channel):
	
		if GPIO.input(channel) == GPIO.LOW:
			while GPIO.input(channel) == GPIO.LOW:
				# while pressed display ip address
				pass

			flash(3)
		
