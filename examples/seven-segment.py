import board, time, threading, atexit
import RPi.GPIO as GPIO

from adafruit_ht16k33.segments import BigSeg7x4
from time import strftime


lights = [[0b00000001, 0b00000000, 0b00000000, 0b00000000],[0b00000000, 0b00000001, 0b00000000, 0b00000000],[0b00000000, 0b00000000, 0b00000001, 0b00000000],[0b00000000, 0b00000000, 0b00000000, 0b00000001],[0b00000000, 0b00000000, 0b00000000, 0b00000010],[0b00000000, 0b00000000, 0b00000000, 0b00000100],[0b00000000, 0b00000000, 0b00000000, 0b00001000],[0b00000000, 0b00000000, 0b00001000, 0b00000000],[0b00000000, 0b00001000, 0b00000000, 0b00000000],[0b00001000, 0b00000000, 0b00000000, 0b00000000],[0b00010000, 0b00000000, 0b00000000, 0b00000000],[0b00100000, 0b00000000, 0b00000000, 0b00000000]]

i2c = board.I2C()
display = BigSeg7x4(i2c, address=0x70)
display.brightness = 1.0



message = "HELLO   "

display.fill(0)
display.marquee(message, 0.25, False)

display.fill(0)
index = 0
		
for loops in range(10):
	for index in range(11):
		display.set_digit_raw(0, lights[index][0])
		display.set_digit_raw(1, lights[index][1])
		display.set_digit_raw(2, lights[index][2])
		display.set_digit_raw(3, lights[index][3])
		time.sleep(.1)

display.fill(0)
display.marquee(message, 0.25, False)

