import board, time, threading, atexit, socket
from time import strftime
from adafruit_ht16k33.segments import BigSeg7x4


i2c = board.I2C()
display = BigSeg7x4(i2c, address=0x70)
display.brightness = 1.0

done = False

def get_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.settimeout(0)
	try:
		# doesn't even have to be reachable
		s.connect(('10.254.254.254', 1))
		IP = s.getsockname()[0]
	except Exception:
		IP = '127.0.0.1'
	finally:
		s.close()
	return IP

def timeLoop():
	
	global done
	
	message = get_ip().replace(".", "-") + "   "
	
	while done == False:
		display.marquee(message, 0.25, False)

	stringTime = "  " + strftime("%-I%M")
	message = get_ip().replace(".", "-") + "    " + stringTime[-5:]
	display.marquee(message, 0.25, False)
	
	stringTime = "  " + strftime("%-I:%M")
	display.print(stringTime[-5:])


clockThread = threading.Thread(target = timeLoop)
clockThread.start()

def shutDown():

	global done
	global clockThread
	
	print("shutting down")

	done = True
	
	clockThread.join()

atexit.register(shutDown)