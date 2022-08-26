from buttons import bigButton
from enum import Enum

class ClockState(Enum):
	HELLO = 0
	TIME = 1
	CHASING = 2
	ADDRESS = 3

class TestThis():

	print("Test This")
	bigButton.flash(2)
	
	state = ClockState.HELLO
	
	def setState(self, state):
		self.state = state
		
	def getState(self):
		return self.state
		
testThis = TestThis()