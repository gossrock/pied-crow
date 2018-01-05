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
from django.utils import timezone

from BellSchedule.models import RingPattern
from BellSchedule.models import Schedule
from BellSchedule.models import EmergencyEvent
from BellSchedule.models import YearCalendar

from BellSchedule.models import get_current_emergency_events


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

def LoadTimes():
	"""
		LoadTimesFile
		
		gets the most recent schedule changes from the django database
	"""
	return_list = []
	sched = YearCalendar.objects.all()[0].todays_schedule()
	if sched is not None:
		bells = sched.bellring_set.all()
		for bell in bells:
			return_list.append({"hour":bell.hour(), "min":bell.minute(), "pattern":bell.ring_pattern})
	return return_list
		
def CheckForEmergency():
	"""
		CheckForEmergency
		
		checks for a change in the database that indicates that an alarm
		is to be sounded.
	"""
	return get_current_emergency_events()
		
def ring_pattern(pattern):
	pattern_parts = pattern.ringpatternpart_set.all()
	for part in pattern_parts:
		duration = part.duration
		if part.on_off == True:
			BELL_SWITCH.onFor(duration)
		else:
			time.sleep(duration)
			

BELLS = LoadTimes() #load the bells file the first time before running

if __name__ == "__main__":
	print_now() # print time at start up
	try:
		while (True): # bell event loop
			
			# emergencies take priority
			emergencies = CheckForEmergency()
			if len(emergencies) > 0: #we have current emergencies
				
				for e in emergencies: # handle one emergency at a time
					all_clear = False
				
					while not all_clear:
						now = timezone.now()
						if e.start_time < now and (e.stop_time is None or e.stop_time > now) and (e.all_clear_time is None or e.all_clear_time > now):
							# in emergency state and bell is active
							ring_pattern(e.emergency_type.ring_pattern)
						elif e.start_time < now and e.stop_time < now and (e.all_clear_time is None or e.all_clear_time > now):
							# in emergency state but bell is silent
							time.sleep(1) # wait a second and check again if we need to give the all clear
						elif e.start_time < now and e.stop_time < now and e.all_clear_time < now:
							time.sleep(1) # wait a second to place a gap before sending all clear patern
							ring_pattern(e.emergency_type.all_clear_pattern)
							all_clear = True
						e.refresh_from_db()
					
			else:
				now = time.localtime()
				hour = now.tm_hour
				minuite = now.tm_min
				sec = now.tm_sec
				if sec == 0: # on the 0th second check to see if there are any bells to ring
					for bell in BELLS:    
						if hour==bell["hour"] and minuite==bell["min"]:
							print_now()
							ring_pattern(bell['pattern'])
				elif sec == 10: # reload the bell list on the 10th second of each min
					 BELLS = LoadTimes()
				else:
					ems = CheckForEmergency()
					for e in ems:
						#obviously this is only proof of concept code.
						print(e.name)
						
			# wait a second and then loop again
			time.sleep(1)

	except KeyboardInterrupt:
		RELAY_BOARD.cleanup()
		print("\nexit")
		print_now()
