import board, time
from adafruit_ht16k33.segments import BigSeg7x4

lights = [[0b00000001, 0b00000000, 0b00000000, 0b00000000],[0b00000000, 0b00000001, 0b00000000, 0b00000000],[0b00000000, 0b00000000, 0b00000001, 0b00000000],[0b00000000, 0b00000000, 0b00000000, 0b00000001],[0b00000000, 0b00000000, 0b00000000, 0b00000010],[0b00000000, 0b00000000, 0b00000000, 0b00000100],[0b00000000, 0b00000000, 0b00000000, 0b00001000],[0b00000000, 0b00000000, 0b00001000, 0b00000000],[0b00000000, 0b00001000, 0b00000000, 0b00000000],[0b00001000, 0b00000000, 0b00000000, 0b00000000],[0b00010000, 0b00000000, 0b00000000, 0b00000000],[0b00100000, 0b00000000, 0b00000000, 0b00000000]]
wakeup = [0b00111100, 0b00011110, 0b01110111, 0b01110110, 0b01111001, 0b00000000, 0b00111110, 0b01110011, 0b00000000]
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

def lightAll():
	display.print("88:88")
	display.top_left_dot = True
	display.bottom_left_dot = True
	display.ampm = True

printHello()
printHello()
printHello()
printHello()
printHello()

for loops in range(10):
	for index in range(11):
		display.set_digit_raw(0, lights[index][0])
		display.set_digit_raw(1, lights[index][1])
		display.set_digit_raw(2, lights[index][2])
		display.set_digit_raw(3, lights[index][3])
		time.sleep(.05)

display.fill(0)

message = "1234567890    "
display.marquee(message, .25, False)

startIndex = 0
for loops in range(20):
	letterIndex = startIndex
	for cellIndex in range(4):
		display.set_digit_raw(cellIndex, wakeup[letterIndex])
		letterIndex += 1
		if letterIndex >= 9:
			letterIndex = 0
		
	time.sleep(.25)
	startIndex += 1
	if startIndex >= 9:
		startIndex = 0

for loops in range(4):
	display.fill(0)
	time.sleep(.25)
	lightAll()
	time.sleep(.25)

time.sleep(4)

display.fill(0)