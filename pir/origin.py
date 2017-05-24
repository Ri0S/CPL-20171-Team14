import RPi.GPIO as GPIO
import time

counter = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)
GPIO.setup(17, GPIO.OUT)

def motionSensor(channel):
	GPIO.output(17, GPIO.LOW)
	if GPIO.input(channel) == 1:
		global counter
		counter += 1
		GPIO.output(17, GPIO.HIGH)
		print "motion: " + str(counter)

GPIO.add_event_detect(4, GPIO.BOTH, callback=motionSensor, bouncetime=150)

try:
	while True:
		time.sleep(0.5)

except KeyboardInterrupt:
	print "inte"

finally:
	GPIO.cleanup()

