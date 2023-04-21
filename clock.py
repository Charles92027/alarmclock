import board, threading, time, socket
from datetime import datetime
from time import strftime
from adafruit_ht16k33.segments import BigSeg7x4
from enum import Enum
from database import database
import buttons

class ClockState(Enum):
	TIME = 0
	HELLO = 1
	CHASING = 2
	ADDRESS = 3
	WAKEUP = 4
	DONE = 5

class ClockFace:

	i2c = None
	display = None
	brightness = 1
	
	state = ClockState.HELLO
	stateThread = None

	def __init__(self):
		self.i2c = board.I2C()
		self.display = BigSeg7x4(self.i2c, address=0x70)
		
		
		row = database.fetchOne("SELECT brightness FROM configuration LIMIT 1;")
		newBrightness = row[0]
		self.brightness = newBrightness
		self.display.brightness = self.brightness

		print("clockface initialized")
		self.stateThread = threading.Thread(target = self.helloState)
		self.stateThread.start()
		
	def setBrightness(self, newBrightness):
		self.brightness = newBrightness
		self.display.brightness = self.brightness
		database.nonQuery("UPDATE configuration SET brightness = {};".format(newBrightness))
		
	def getBrightness(self):
		return self.brightness
	
	def clear(self):
		self.display.fill(0)
		
	def printHello(self):
		self.display.set_digit_raw(0, 0b01110110)
		self.display.set_digit_raw(1, 0b01111001)
		self.display.set_digit_raw(2, 0b00110110)
		self.display.set_digit_raw(3, 0b00111111)
	
	def helloState(self):
	
		print("clockFace State = ", self.state)
	
		self.printHello()
		while(self.state == ClockState.HELLO):
			time.sleep(.5)
		
		self.nextState()
		
	def timeState(self):
	
		print("clockFace State = ", self.state)
	
		self.clear()
		
		while(self.state == ClockState.TIME):
		
			try:
				stringTime = "  " + strftime("%-I:%M")
				self.display.print(stringTime[-5:])
				self.display.ampm = (datetime.now().hour >= 12)
				
				from alarm import alarm
				self.display.bottom_left_dot = alarm.alarmPending()
				
				time.sleep(.5)
			except:
				pass

		self.nextState()
	
	def chasingState(self):
	
		print("clockFace State = ", self.state)
	
		lights = [
			[0b00000001, 0b00000000, 0b00000000, 0b00000000],[0b00000000, 0b00000001, 0b00000000, 0b00000000],
			[0b00000000, 0b00000000, 0b00000001, 0b00000000],[0b00000000, 0b00000000, 0b00000000, 0b00000001],
			[0b00000000, 0b00000000, 0b00000000, 0b00000010],[0b00000000, 0b00000000, 0b00000000, 0b00000100],
			[0b00000000, 0b00000000, 0b00000000, 0b00001000],[0b00000000, 0b00000000, 0b00001000, 0b00000000],
			[0b00000000, 0b00001000, 0b00000000, 0b00000000],[0b00001000, 0b00000000, 0b00000000, 0b00000000],
			[0b00010000, 0b00000000, 0b00000000, 0b00000000],[0b00100000, 0b00000000, 0b00000000, 0b00000000]]
	
		self.clear()
		index = 0
		
		while(self.state == ClockState.CHASING):
			self.display.set_digit_raw(0, lights[index][0])
			self.display.set_digit_raw(1, lights[index][1])
			self.display.set_digit_raw(2, lights[index][2])
			self.display.set_digit_raw(3, lights[index][3])
			time.sleep(.1)
				
			index = index + 1
			if (index > 11):
				index = 0

		self.nextState()
	
	def addressState(self):
	
		print("clockFace State = ", self.state)
	
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
		
		while(self.state == ClockState.ADDRESS):
			self.display.marquee(message, 0.25, False)
		
		stringTime = "  " + strftime("%-I%M")
		message = message + stringTime[-5:]
		self.display.marquee(message, 0.25, False)	
	
		self.nextState()
	
	def wakeUpState(self):
	
		wakeup = [0b00111100, 0b00011110, 0b01110111, 0b01110110, 0b01111001, 0b00000000, 0b00111110, 0b01110011, 0b00000000]

		self.clear()
		startIndex = 0
		
		while(self.state == ClockState.WAKEUP):
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
		
		self.nextState()
		
	def nextState(self):
	
		if self.state == ClockState.HELLO:
			self.stateThread = threading.Thread(target = self.helloState)
			self.stateThread.start()
			
		elif self.state == ClockState.CHASING:
			self.stateThread = threading.Thread(target = self.chasingState)
			self.stateThread.start()
	
		elif self.state == ClockState.ADDRESS:
			self.stateThread = threading.Thread(target = self.addressState)
			self.stateThread.start()
			
		elif self.state == ClockState.WAKEUP:
			self.stateThread = threading.Thread(target = self.wakeUpState)
			self.stateThread.start()
			
		elif self.state == ClockState.DONE:
			print("stopping the clock")
			self.clear()

		else:
			self.stateThread = threading.Thread(target = self.timeState)
			self.stateThread.start()	
	
	def hello(self):
		self.state = ClockState.HELLO
		
	def chase(self):
		self.state = ClockState.CHASING
		
	def address(self):
		self.state = ClockState.ADDRESS
		
	def time(self):
		self.state 	= ClockState.TIME
	
	def wakeUp(self):
		self.state = ClockState.wakeUp
	
	def done(self):
		self.state = ClockState.DONE
		self.stateThread.join()
	
	def setState(self, state):
	
		self.state = state
		if self.state == ClockState.DONE:
			self.stateThread.join()
		
clockFace = ClockFace()