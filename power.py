import RPi.GPIO as GPIO
import buttons

class PowerState:

	powerPin = 24
	lowBatteryPin = 6
	
	def __init__(self):

		GPIO.setup(self.powerPin, GPIO.IN)
		GPIO.setup(self.lowBatteryPin, GPIO.IN)

	def hasPower(self):
		return GPIO.input(self.powerPin) == GPIO.LOW
	
	def lowBattery(self):
		return GPIO.input(self.lowBatteryPin) == GPIO.HIGH

powerState = PowerState()

