import time, threading
from database import database
from buttons import bigButton
from datetime import datetime
from enum import Enum

class AlarmState(Enum):
	QUIET = 0
	ALARM = 1
	ESCALATION = 2

class Alarm:

	state = AlarmState.QUIET
	stateThread = None
	
	lastAlarmId = None
	
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
		
		startTicking = 0
	
		while(self.state == AlarmState.QUIET):
			
			time.sleep(.1)
		
			#reload the data every 5 minutes
			elapsed = time.time() - startTicking
			if elapsed > 300:
				recordset = database.getNextAlarm()
				if recordset is not None:
					self.nextAlarmId, self.nextAlarmDate, self.nextAlarmTime, self.nextAlarmDateTime, self.nextAlarmSound = recordset
					self.nextAlarmDateTime = xTime = datetime.strptime(self.nextAlarmDateTime, "%Y-%m-%d %H:%M:%S")
					print(self.nextAlarmId, self.nextAlarmDate, self.nextAlarmTime, self.nextAlarmDateTime, self.nextAlarmSound)
				startTicking = time.time()

			if self.lastAlarmId != self.nextAlarmId:

				rightNow = datetime.now()
				interval = rightNow - self.nextAlarmDateTime
				interMinutes = interval.total_seconds() / 60

				if interMinutes > 0:
					self.lastAlarmId = self.nextAlarmId
					print("ALARMING")
					#self.state = AlarmState.ALARM

		self.nextState()

	def alarmState(self):

		print("alarm state State = ", self.state)
	
		# start music playing
	
		while(self.state == AlarmState.ALARM):
			bigButton.flash(1)	# this replaces our timer
			# a button press will change the state back to quiet
			# if too much time has passed since the alarm started, trnasition to the ESCALATION state
		
		self.nextState()

	def escalationState(self):

		print("alarm state State = ", self.state)
	
		# stop the 
	
		while(self.state == AlarmState.ALARM):
			time.sleep(.1)
			# a button press will change the state back to quiet
			# if too much time has passed since the alarm started, trnasition to the ESCALATION state
		
		self.nextState()


	def nextState(self):
	
		if self.state == AlarmState.QUIET:
			self.stateThread = threading.Thread(target = self.quietState)
			self.stateThread.start()
			
		elif self.state == AlarmState.ALARM:
			self.stateThread = threading.Thread(target = self.alarmState)
			self.stateThread.start()
	
		elif self.state == AlarmState.ESCALATION:
			self.stateThread = threading.Thread(target = self.escalationState)
			self.stateThread.start()

		else:
			self.stateThread = threading.Thread(target = self.quietState)
			self.stateThread.start()


alarm = Alarm()