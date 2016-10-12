#! /usr/bin/python
"""
	bell_controler
	
	This is the script that runs to control the Bell atached to the relay
	switch atached to the Raspberry Pi. Currently it only can ring 1 bell
	atached to Relay Switch 1 (or Relay Switch 2 when in DEBUG mode)
"""
import PiSwitches as PiSwitches
import time

# this chunk is related to getting this to work with django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'PiedCrow.settings'
import django
django.setup()


# importing the django classes that relate to ringing the bell
from BellSchedule.models import Schedule
from BellSchedule.models import EmergencyBells


RELAY_BOARD = PiSwitches.FourPortRelaySwitch()

DEBUG = False
BELL_SWITCH = None
TIME_FILE = ''

if DEBUG == False:
	print("**** Normal Operation ****")
	BELL_SWITCH = RELAY_BOARD.s1
	TIME_FILE = "/home/peter/Desktop/bell/bell_list"
elif DEBUG == True:
	print("**** DEBUGING MODE ****")
	BELL_SWITCH = RELAY_BOARD.s2
	TIME_FILE = "/home/peter/Desktop/bell/debug_bell_list"
print("DEBUGING == "+str(DEBUG))


def print_now():
	"""
		print_now
		
		a utility function to print the current time. Mostly for development
		and debuging purposes
	"""
	print(time.strftime("The time is %H:%M:%S"))

def LoadTimesFile():
	"""
		LoadTimesFile
		
		gets the most recent schedule changes from the django database
	"""
	return_list = []
	sched = Schedule.objects.get(pk=1) #needs to be updated so that it will figure out the current day's schedule
	bells = sched.bellring_set.all()
	for bell in bells:
		return_list.append({"hour":bell.hour(), "min":bell.minute()})
	return return_list
		
def CheckForEmergency():
	"""
		CheckForEmergency
		
		checks for a change in the database that indicates that an alarm
		is to be sounded.
	"""
	return EmergencyBells.objects.filter(active=True)
		
		

BELLS = LoadTimesFile(TIME_FILE) #load the bells file the first time before running
BELLDURATION=4 #duration of a normal bell ring. needs to be updated to work with the database

if __name__ == "__main__":
	print_now() # print time at start up
	try:
		while (True):
			now = time.localtime()
			hour = now.tm_hour
			minuite = now.tm_min
			sec = now.tm_sec
			if sec == 0: # on the 0th second check to see if there are any bells to ring
				for bell in BELLS:    
					if hour==bell["hour"] and minuite==bell["min"]:
						print_now()
						BELL_SWITCH.onFor(BELLDURATION)
			elif sec == 10: # reload the bell list on the 10th second of each min
				 BELLS = LoadTimesFile(TIME_FILE)
			else:
				ems = CheckForEmergency()
				for e in ems:
					#obviously this is only proof of concept code.
					print(e.name)
			time.sleep(1)

	except KeyboardInterrupt:
		RELAY_BOARD.cleanup()
		print("\nexit")
		print_now()
