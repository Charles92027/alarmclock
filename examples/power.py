import time, RPi.GPIO as GPIO, board
from adafruit_ht16k33.segments import BigSeg7x4
from datetime import timedelta

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

powerPin = 24
lowBatteryPin = 6	# big button for now

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(powerPin, GPIO.IN)
GPIO.setup(lowBatteryPin, GPIO.IN)

i2c = board.I2C()
display = BigSeg7x4(i2c, address=0x70)
display.fill(0)
brightness = 1.00
display.brightness = brightness

lights = [[0b00000001, 0b00000000, 0b00000000, 0b00000000],[0b00000000, 0b00000001, 0b00000000, 0b00000000],[0b00000000, 0b00000000, 0b00000001, 0b00000000],[0b00000000, 0b00000000, 0b00000000, 0b00000001],[0b00000000, 0b00000000, 0b00000000, 0b00000010],[0b00000000, 0b00000000, 0b00000000, 0b00000100],[0b00000000, 0b00000000, 0b00000000, 0b00001000],[0b00000000, 0b00000000, 0b00001000, 0b00000000],[0b00000000, 0b00001000, 0b00000000, 0b00000000],[0b00001000, 0b00000000, 0b00000000, 0b00000000],[0b00010000, 0b00000000, 0b00000000, 0b00000000],[0b00100000, 0b00000000, 0b00000000, 0b00000000]]

index = 0
while GPIO.input(powerPin) == GPIO.LOW:

	display.set_digit_raw(0, lights[index][0])
	display.set_digit_raw(1, lights[index][1])
	display.set_digit_raw(2, lights[index][2])
	display.set_digit_raw(3, lights[index][3])
	time.sleep(.05)
	index = index + 1
	if index > 10:
		index = 0

start = time.time()

while GPIO.input(lowBatteryPin) == GPIO.LOW and GPIO.input(powerPin) == GPIO.HIGH:

	end = time.time()
	elapsed = (end - start)
	
	hours, rem = divmod(elapsed, 3600)
	minutes, seconds = divmod(rem, 60)
	mask = "{:0>2}:{:0>2}"
	stringTime = mask.format(int(hours), int(minutes))
	
	display.print(stringTime)