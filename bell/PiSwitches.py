"""
	PiSwitches
	
	This module abstracts the working of a 4 port Switch.
"""

import time

try:
	# default operation is te import the real RPi.GPIO module
	import RPi.GPIO as GPIO
except ImportError:
	# if it doesn't exist (like in my development VM) use my stub instead
	import StubGPIO as GPIO


DEFAULT_PINS=[2,3,4,17]

class FourPortRelaySwitch(object):
	"""
		FourPortRelaySwitch
		
		This class represents the 4 port Reay Switch attached to the 
		Raspberry Pi. It can be used to setup and keep track of the 4 
		RelaySwitch objects representing the indevidual switches on the 
		board.
	"""
	s1 = None 
	s2 = None
	s3 = None
	s4 = None
	
	def __init__(self, switch_pins=DEFAULT_PINS):
		"""
			__init__
			
			takes a list of Pin numbers or uses a default set [2,3,4,17] 
			if a list is not provided.
		"""
		GPIO.setmode(GPIO.BCM)
		self.s1 = RelaySwitch(switch_pins[0])
		self.s2 = RelaySwitch(switch_pins[1])
		self.s3 = RelaySwitch(switch_pins[2])
		self.s4 = RelaySwitch(switch_pins[3])
		
	def cleanup(self):
		"""
			cleanup
			
			Should be called when the program shuts down.
		"""
		GPIO.cleanup()
	
class RelaySwitch(object):
	"""
		RelaySwitch
		
		Represents an indevidual switch on the RelaySwitch board and gives
		conveniantly named methods to turn the switches on and off. All
		methods assume that you have connected the switchs so that they 
		are usually off.
	"""
	gpio_pin = None

	def __init__(self, gpio_pin):
		"""
			__init__
			
			sets the GPIO pin up for oporation with the Relay Switch			
		"""
		self.gpio_pin = gpio_pin
		GPIO.setup(self.gpio_pin, GPIO.OUT)
		self.off()
	
	def on(self):
		"""
			on
			
			turns the switch to the on position. (assumes "usually off" connection)
		"""
		GPIO.output(self.gpio_pin, GPIO.LOW)
	
	def off(self):
		"""
			off
			
			turns the switch to the off position. (assumes "usually off" connection)
		"""
		GPIO.output(self.gpio_pin, GPIO.HIGH)

	def onFor(self, seconds):
		"""
			onFor
			
			takes a number of decimal seconds and will turn the switch on
			for that specified duration. In it's current implementation 
			it will block all other switch actions. (assumes "usually off" connection)
		"""
		try:
			float(seconds)
			self.on()
			time.sleep(seconds)
			self.off()
		except ValueError:
			pass




if __name__ == "__main__":
	# quick test
	FPR = FourPortRelaySwitch()
	FPR.s1.onFor(1.5)
	FPR.s1.on()
	FPR.cleanup()
	
	
