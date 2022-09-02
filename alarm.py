import time, threading
from database import database
from buttons import bigButton
from datetime import datetime
from enum import Enum
from sounds import player

class AlarmState(Enum):
	QUIET = 0
	ALARM = 1
	ESCALATION = 2

class Alarm:

	state = AlarmState.QUIET
	stateThread = None
	
	lastAlarmId = None
	lastAlarmDateTime = None
	
	nextAlarmId = None
	nextAlarmDate = None
	nextAlarmTime = None
	nextAlarmDateTime = None
	nextAlarmSound = None

	def __init__(self):

		print("alarm initialized")
		
		self.stateThread = threading.Thread(target = self.quietState)
		self.stateThread.start()

	def quietState(self):
	
		print("alarm state State = ", self.state)
		
		player.stop()
		startTicking = 0
	
		while(self.state == AlarmState.QUIET):
			
			time.sleep(.1)
		
			#reload the data every minute
			elapsed = time.time() - startTicking
			if elapsed > 60:
				recordset = database.getNextAlarm()
				if recordset is not None:
					self.nextAlarmId, self.nextAlarmDate, self.nextAlarmTime, self.nextAlarmDateTime, self.nextAlarmSound = recordset
					self.nextAlarmDateTime = xTime = datetime.strptime(self.nextAlarmDateTime, "%Y-%m-%d %H:%M:%S")
					print(self.nextAlarmId, self.nextAlarmDate, self.nextAlarmTime, self.nextAlarmDateTime, self.nextAlarmSound)
				startTicking = time.time()

			if self.lastAlarmDateTime != self.nextAlarmDateTime:

				rightNow = datetime.now()
				interval = rightNow - self.nextAlarmDateTime
				interMinutes = interval.total_seconds() / 60

				if interMinutes >= 0:
					self.state = AlarmState.ALARM

		self.nextState()

	def alarmState(self):

		print("alarm state State = ", self.state)
	
		self.lastAlarmDateTime = self.nextAlarmDateTime
		startTicking = time.time()
	
		# a button press will change the state back to quiet			
		while(self.state == AlarmState.ALARM):

			if player.playng() == False:
				player.play(nextAlarmSound)

			bigButton.flash(1)	# this replaces our timer
			
			# if too much time has passed since the alarm started, transition to the ESCALATION state
			elapsed = time.time() - startTicking
			if elapsed > 120:			
				self.state == AlarmState.ESCALATION

		self.nextState()

	def escalationState(self):

		print("alarm state State = ", self.state)
	
		# do something big here
		# increase the volume, flash the display
	
		while(self.state == AlarmState.ALARM):
			bigButton.flash(1)	# this replaces our timer
			# a button press will change the state back to quiet
		
		self.nextState()

	def bigButtonPressed(self):
		
		if self.state == AlarmState.ALARM or self.state == AlarmState.ESCALATION:
			self.state = AlarmState.QUIET

		else:
			pass
			# if an alarm is due within the next 60 minutes then 
			# wait until the button has been held for 5 seconds then
			# flash the button three times
			# and clear the next alarm

	def nextState(self):
	
		if self.state == AlarmState.ALARM:
			self.stateThread = threading.Thread(target = self.alarmState)
			self.stateThread.start()
	
		elif self.state == AlarmState.ESCALATION:
			self.stateThread = threading.Thread(target = self.escalationState)
			self.stateThread.start()

		#if self.state == AlarmState.QUIET:
		else:
			self.stateThread = threading.Thread(target = self.quietState)
			self.stateThread.start()


alarm = Alarm()
