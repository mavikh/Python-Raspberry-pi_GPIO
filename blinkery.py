#In this program we do an input, output and PWM handlings.
#if Push-Button pressed --> blink LED2 with delay 0.5s
#otherwise turn on LED1 using software PWM
#Turn off both LEDs if CTRL+C is pressed on keyboard

# External module imports
import RPi.GPIO as GPIO
from time import sleep

# Pin Definition:
led1Pin = 11 # GPIO17
led2Pin = 16 # GPIO23
buttonPin = 15 # GPIO22

# Pin Setup:
GPIO.setmode(GPIO.BOARD) # Physical header pin-numbering scheme
GPIO.setup(led1Pin, GPIO.OUT) # LED1 pin set as output
pwm = GPIO.PWM(led1Pin,100) # Initialize PWM on led1Pin 100Hz(period:10ms)
GPIO.setup(led2Pin, GPIO.OUT) # LED2 pin as output
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button as input and is pulled up
pwm.start(50) # Duty cycle = 50%
 
print("Press CTRL+C to stop!")
try:
        
	while(1):
		if GPIO.input(buttonPin): # button released
			GPIO.output(led2Pin, GPIO.LOW) # LED2 off
			pwm.ChangeDutyCycle(50) # Turns on LED1 with Duty cycle = 50%
		else: # button is pressed
			pwm.ChangeDutyCycle(1) # decrease duty cycle value to dim LED1
			GPIO.output(led2Pin, GPIO.HIGH) # LED2 on1
			sleep(0.5) # 0.5S delay
			GPIO.output(led2Pin, GPIO.LOW) # LED2 off
			sleep(0.5)
except KeyboardInterrupt: # if Ctrl+C is pressed
	pwm.stop()
	GPIO.cleanup() # clean up all GPIO
