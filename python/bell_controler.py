#! /usr/bin/python
import PiSwitchesStubs as PiSwitches
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

# utility function to print time
def print_now():
	print(time.strftime("The time is %H:%M:%S"))

def LoadTimesFile(filename):
	return_list = []
	f = open(filename, 'r')
	for line in f:
		#print(line)
		hour, minuite = line.split(":")
		return_list.append({"hour":int(hour), "min":int(minuite)})
	#print(return_list)
	return return_list
		
BELLS = LoadTimesFile(TIME_FILE)

BELLDURATION=4

if __name__ == "__main__":
	
	print_now() # print time at start up
	try:
		while (True):
			now = time.localtime()
			hour = now.tm_hour
			minuite = now.tm_min
			sec = now.tm_sec
			if sec == 0:
				for bell in BELLS:    
					if hour==bell["hour"] and minuite==bell["min"]:
						#print(bell)
						print_now()
						BELL_SWITCH.onFor(BELLDURATION)
			elif sec == 10: # reload the bell list on the 10th second of each min
				 #print("reloading")	
				 BELLS = LoadTimesFile(TIME_FILE)
			time.sleep(1)

	except KeyboardInterrupt:
		RELAY_BOARD.cleanup()
		print("exit")
		print_now()
