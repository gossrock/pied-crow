import time

#import RPi.GPIO as GPIO

FORMAT = "%H:%M:%S"

DEFAULT_PINS=[2,3,4,17]

class FourPortRelaySwitch(object):
	s1 = None 
	s2 = None
	s3 = None
	s4 = None
	
	def __init__(self, switch_pins=DEFAULT_PINS):
		print("setting up Relay switch."+str(switch_pins))
		#GPIO.setmode(GPIO.BCM)
		self.s1 = RelaySwitch("Switch 1", switch_pins[0])
		self.s2 = RelaySwitch("Switch 2", switch_pins[1])
		self.s3 = RelaySwitch("Switch 3", switch_pins[2])
		self.s4 = RelaySwitch("Switch 4", switch_pins[3])
		
	def cleanup(self):
		print("cleaning up")
		#GPIO.cleanup()
	
class RelaySwitch(object):
	name = ""
	gpio_pin = None

	def __init__(self, name, gpio_pin):
		self.name = name
		self.gpio_pin = gpio_pin
		print("setting up "+name+" on GPIO pin "+str(gpio_pin))
		#GPIO.setup(self.gpio_pin, GPIO.OUT)
		self.off()
	
	def on(self):
		print(time.strftime("%H:%M:%S")+" turning on "+self.name)
		#GPIO.output(self.gpio_pin, GPIO.LOW)
	
	def off(self):
		print(time.strftime("%H:%M:%S")+" turning off "+self.name)
		#GPIO.output(self.gpio_pin, GPIO.HIGH)

	def onFor(self, seconds):
		try:
			float(seconds)
			self.on()
			time.sleep(seconds)
			self.off()
		except ValueError:
			pass




if __name__ == "__main__":
	FPR = FourPortRelaySwitch()
	FPR.s1.onFor(1.5)
	FPR.s1.on()
	FPR.cleanup()
	
	
