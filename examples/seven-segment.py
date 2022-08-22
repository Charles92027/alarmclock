import board, time
from adafruit_ht16k33.segments import BigSeg7x4

lights = [[0b00000001, 0b00000000, 0b00000000, 0b00000000],[0b00000000, 0b00000001, 0b00000000, 0b00000000],[0b00000000, 0b00000000, 0b00000001, 0b00000000],[0b00000000, 0b00000000, 0b00000000, 0b00000001],[0b00000000, 0b00000000, 0b00000000, 0b00000010],[0b00000000, 0b00000000, 0b00000000, 0b00000100],[0b00000000, 0b00000000, 0b00000000, 0b00001000],[0b00000000, 0b00000000, 0b00001000, 0b00000000],[0b00000000, 0b00001000, 0b00000000, 0b00000000],[0b00001000, 0b00000000, 0b00000000, 0b00000000],[0b00010000, 0b00000000, 0b00000000, 0b00000000],[0b00100000, 0b00000000, 0b00000000, 0b00000000]]

i2c = board.I2C()
display = BigSeg7x4(i2c, address=0x70)
display.brightness = 1.0

def printHello():
	time.sleep(.2)
	display.set_digit_raw(0, 0b01110110)
	display.set_digit_raw(1, 0b01111001)
	display.set_digit_raw(2, 0b00110110)
	display.set_digit_raw(3, 0b00111111)
	time.sleep(.2)
	display.fill(0)

printHello()
printHello()
printHello()
printHello()
printHello()

for loops in range(4):
	for index in range(11):
		display.set_digit_raw(0, lights[index][0])
		display.set_digit_raw(1, lights[index][1])
		display.set_digit_raw(2, lights[index][2])
		display.set_digit_raw(3, lights[index][3])
		time.sleep(.1)

display.fill(0)

message = "1234567890    "
display.marquee(message, .25, False)
