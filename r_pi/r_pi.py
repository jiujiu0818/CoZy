import RPi.GPIO as GPIO 

class Sim_ThermoStat(object):

    def __init__(self):
        self.on = 0
        GPIO.setmode(GPIO.BCM) 
        # Set up the pin you are using. 18 in this case 
        GPIO.setup(18, GPIO.OUT) 
        self.target = ''
    
    def turn_on(self):
        # Turn on the pin and see the LED light up. 
        GPIO.output(18, GPIO.HIGH) 
        self.on = 1

    def turn_off(self):
        GPIO.output(18, GPIO.LOW)
        self.on = 0

    def get_temp(self):
        tfile = open("/sys/bus/w1/devices/28-00000554bd80/w1_slave") 
        text = tfile.read() 
        tfile.close() 
        secondline = text.split("\n")[1] 
        temperaturedata = secondline.split(" ")[9] 
        temperature = float(temperaturedata[2:]) 
        temperature = temperature / 1000 
        return temperature

    def set_temp(self, target_temp):
        # sets the global temp for this thermostat
        print 'thermostat set to ' + str(target_temp)
        self.target = int(target_temp)
        self.check

    def check(self):
        if get_temp() > self.target and self.on == 1:
            self.turn_off
        elif get_temp() < self.target and self.on == 0:
            self.turn_on