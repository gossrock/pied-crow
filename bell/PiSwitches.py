import time

try:
	import RPi.GPIO as GPIO
except ImportError:
	import StubGPIO as GPIO


DEFAULT_PINS=[2,3,4,17]

class FourPortRelaySwitch(object):
    s1 = None 
    s2 = None
    s3 = None
    s4 = None
	
    def __init__(self, switch_pins=DEFAULT_PINS):
        GPIO.setmode(GPIO.BCM)
        self.s1 = RelaySwitch(switch_pins[0])
        self.s2 = RelaySwitch(switch_pins[1])
        self.s3 = RelaySwitch(switch_pins[2])
        self.s4 = RelaySwitch(switch_pins[3])
        
    def cleanup(self):
        GPIO.cleanup()
	
class RelaySwitch(object):
    gpio_pin = None

    def __init__(self, gpio_pin):
        self.gpio_pin = gpio_pin
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        self.off()
    
    def on(self):
        GPIO.output(self.gpio_pin, GPIO.LOW)
	
    def off(self):
        GPIO.output(self.gpio_pin, GPIO.HIGH)

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
    
    
