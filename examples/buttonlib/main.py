import threading, atexit
from buttons import bigButton
from buttons import littleButton

from second import testThis
from second import ClockState

done = False


print("testThis.state = ", testThis.getState())
testThis.setState(ClockState.TIME)
print("testThis.state = ", testThis.getState())
testThis.setState(ClockState.CHASING)
print("testThis.state = ", testThis.getState())
testThis.setState(ClockState.ADDRESS)
print("testThis.state = ", testThis.getState())
testThis.setState(ClockState.HELLO)
print("testThis.state = ", testThis.getState())



def waitForDone():

	global done
	
	while done == False:
		pass
	




waitThread = threading.Thread(target = waitForDone)
waitThread.start()

def shutDown():

	global done
	global waitThread

	print("shutting down")

	done = True
	waitThread.join()

	GPIO.cleanup()

atexit.register(shutDown)
