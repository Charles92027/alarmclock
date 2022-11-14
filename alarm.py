import time, threading
from datetime import datetime
from enum import Enum
from sounds import player

from database import database
import buttons, clock

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

	def loadNextAlarm(self):
		recordset = database.getNextAlarm()
		if recordset is None:
			self.nextAlarmId = 0
			# self.nextAlarmDate = self.nextAlarmTime = self.nextAlarmDateTime = self.nextAlarmSound = null
		else:
			self.nextAlarmId, self.nextAlarmDate, self.nextAlarmTime, self.nextAlarmDateTime, self.nextAlarmSound = recordset
			self.nextAlarmDateTime = datetime.strptime(self.nextAlarmDateTime, "%Y-%m-%d %H:%M:%S")
			print(self.nextAlarmId, self.nextAlarmDate, self.nextAlarmTime, self.nextAlarmDateTime, self.nextAlarmSound)

	def quietState(self):
	
		print("alarm state State = ", self.state)
		
		player.stop()
		player.play("silence.mp3")		# player.stop isn't working for some reason
		startTicking = 0
	
		while(self.state == AlarmState.QUIET):
			
			time.sleep(.1)
		
			#reload the data every ten seconds
			elapsed = time.time() - startTicking
			if elapsed > 10:
				self.loadNextAlarm()
				#print(self.nextAlarmId, self.nextAlarmDate, self.nextAlarmTime, self.nextAlarmDateTime, self.nextAlarmSound)
				startTicking = time.time()

			if self.nextAlarmId > 0:

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

			if player.playing() == False:
				player.play(self.nextAlarmSound)

			buttons.bigButton.flash(1)	# this replaces our timer
			
			# if too much time has passed since the alarm started, transition to the ESCALATION state
			elapsed = time.time() - startTicking
			if elapsed > 120:
				self.state == AlarmState.ESCALATION

		self.nextState()

	def alarmPending(self):
	
		rval = False
		
		if self.nextAlarmId:
			rightNow = datetime.now()
			interval = self.nextAlarmDateTime - rightNow
			totalSeconds = interval.total_seconds()
			
			if totalSeconds <= 3600:
				rval = True
			
		return rval


	def escalationState(self):

		print("alarm state State = ", self.state)
	
		clock.clockFace.wakeUp()
	
		while(self.state == AlarmState.ESCALATION):
			bigButton.flash(1)	# this replaces our timer
		
		clock.clockFace.time()
		
		self.nextState()

	def bigButtonPressed(self):

		if self.state == AlarmState.ALARM or self.state == AlarmState.ESCALATION:
			self.state = AlarmState.QUIET

		else:

			# if an alarm is due within the next 60 minutes then 
			# wait until the button has been held for 3 seconds then
			# flash the button three times
			# and clear the next alarm
			if self.alarmPending():
				rightNow = datetime.now()
				while buttons.bigButton.isPressed():
				
					interval = datetime.now() - rightNow
					if interval.total_seconds() >= 3:
						buttons.bigButton.flash(3)
						database.skipAlarmToday(self.nextAlarmId)
						self.loadNextAlarm()
			
	def bigButtonReleased(self):
		pass


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
