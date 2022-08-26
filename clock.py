import board, threading, time, socket
from time import strftime
from adafruit_ht16k33.segments import BigSeg7x4
from enum import Enum

class ClockState(Enum):
	TIME = 0
	HELLO = 1
	CHASING = 2
	ADDRESS = 3

class Face:

	i2c = None
	display = None
	
	state = ClockState.HELLO
	
	stateThread = None
	changeState = False

	def __init__(self):
		self.i2c = board.I2C()
		self.display = BigSeg7x4(i2c, address=0x70)
		self.display.brightness = 1.0

		self.stateThread = threading.Thread(target = self.helloState)
		self.stateThread.start()
		
	def setBrightness(self, brightness):
		self.display.brightness = brightness
	
	def clear(self):
		self.display.fill(0)
		
	def helloState(self):
		self.clear)()
		self.display.set_digit_raw(0, 0b01110110)
		self.display.set_digit_raw(1, 0b01111001)
		self.display.set_digit_raw(2, 0b00110110)
		self.display.set_digit_raw(3, 0b00111111)
		while(self.changeState == False):
			time.sleep(.5)
		
	def timeState(self):
		self.clear)()
		while(self.changeState == False):
			stringTime = "  " + strftime("%-I:%M")
			self.display.print(stringTime[-5:])
			time.sleep(.5)
	
	def chasingState(self):
	
		lights = [
			[0b00000001, 0b00000000, 0b00000000, 0b00000000],[0b00000000, 0b00000001, 0b00000000, 0b00000000],
			[0b00000000, 0b00000000, 0b00000001, 0b00000000],[0b00000000, 0b00000000, 0b00000000, 0b00000001],
			[0b00000000, 0b00000000, 0b00000000, 0b00000010],[0b00000000, 0b00000000, 0b00000000, 0b00000100],
			[0b00000000, 0b00000000, 0b00000000, 0b00001000],[0b00000000, 0b00000000, 0b00001000, 0b00000000],
			[0b00000000, 0b00001000, 0b00000000, 0b00000000],[0b00001000, 0b00000000, 0b00000000, 0b00000000],
			[0b00010000, 0b00000000, 0b00000000, 0b00000000],[0b00100000, 0b00000000, 0b00000000, 0b00000000]]
	
		self.clear()
		index = 0
		
		while(self.changeState == False):
			self.display.set_digit_raw(0, lights[index][0])
			self.display.set_digit_raw(1, lights[index][1])
			self.display.set_digit_raw(2, lights[index][2])
			self.display.set_digit_raw(3, lights[index][3])
			time.sleep(.1)
				
			index = index + 1
			if (index > 11):
				index = 0
			
	def addressState(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.settimeout(0)

		try:
			sock.connect(('10.254.254.254', 1))
			ipAddress = sock.getsockname()[0]
		except:
			ipAddress = '10.10.10.10'		# hotspot on
		finally:
			sock.close()

		message = ipAddress.replace(".", "-") + "   "
		
		while(self.changeState == False):
			display.marquee(message, 0.25, False)
		
		stringTime = "  " + strftime("%-I%M")
		message = message + stringTime[-5:]
		display.marquee(message, 0.25, False)	
	
	def setState(self, state):
		self.changeState = True
		self.stateThread.join()
		
		self.state = state
		
		if self.state == ClockState.HELLO:
			self.stateThread = threading.Thread(target = self.helloState)

		elif self.state == ClockState.CHASING:
			self.stateThread = threading.Thread(target = self.chasingState)
	
		elif self.state == ClockState.ADDRESS:
			self.stateThread = threading.Thread(target = self.addressState)
			
		else:
			self.stateThread = threading.Thread(target = self.timeState)

		
face = Face()