# a set of basicly "do nothing" stubs to use while running on a system
# that does not have the RPi.GPIO module installed. This should not happen
# while running this on a RaspberryPi. I have only included the parts that
# I personally use at this point.
print ("STUB GPIO: You are not using the real RPi.GPIO module.")


BCM = "BCM"
OUT = "OUTPUT"
HIGH = "HIGH"
LOW = "LOW"


def setmode(mode):
	print("STUB GPIO: setting mode "+mode)

def setup(pin, out):
	print("STUB GPIO: setting up pin "+str(pin)+" as "+out)
	
def output(pin, level):
	print ("STUB GPIO: setting pin "+str(pin)+" to "+ level)
	
def cleanup():
	print ("STUB GPIO: cleaning up")
	
	
