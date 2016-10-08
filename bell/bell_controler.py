#! /usr/bin/python
"""
	bell_controler
	
	This is the script that runs to control the Bell atached to the relay
	switch atached to the Raspberry Pi. Currently it only can ring 1 bell
	atached to Relay Switch 1 (or Relay Switch 2 when in DEBUG mode)
"""
import PiSwitches as PiSwitches
import time


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

def LoadTimesFile(filename):
	"""
		LoadTimesFile
		
		exspects a file name (including the path) for the file containing
		the times when the bell should ring. The file should be formated
		with a time on each line in 24 hour time (ex 14:30)
	"""
	return_list = []
	f = open(filename, 'r')
	for line in f:
		hour, minuite = line.split(":")
		return_list.append({"hour":int(hour), "min":int(minuite)})
	return return_list
		
BELLS = LoadTimesFile(TIME_FILE) #load the bells file the first time before running

BELLDURATION=4 #duration of a normal bell ring.

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
			time.sleep(1)

	except KeyboardInterrupt:
		RELAY_BOARD.cleanup()
		print("\nexit")
		print_now()
