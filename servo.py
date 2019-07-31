# In this program a servo is controlled by pwm to move to its different angles.
# import external modules
import RPi.GPIO as IO 
import time

# set pins
IO.setmode(IO.BOARD) # use pin numbers on the board
IO.setup(11, IO.OUT) # set pin 11(GPIO17) as output
pwm = IO.PWM(11, 50) # initialize pwm on pin 11 to frequency 50

while(1):
	for desired_angle in range (0, 180)
		dc = 2./45. * desired_angel + 2 # duty cycle
		pwm.ChangeDutyCycle(dc)
		sleep(.01)
	for desired_angle in range(180, 0, -1)
		dc = 2./45. * desired_angle + 2 # duty cycle
		pwm.ChangeDutyCycle(dc)
		sleep(.01)
pwm.stop()
IO.cleanup() 
