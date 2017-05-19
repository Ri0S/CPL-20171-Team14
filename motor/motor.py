import RPi.GPIO as GPIO
import time

pin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
p = GPIO.PWM(pin, 50)
p.start(0)
cnt = 0

try:
	while True:
		p.ChangeDutyCycle(8)
		print "angle : 1"
		time.sleep(0.5)
		p.ChangeDutyCycle(0)
		time.sleep(0.5)
except KeyboardInterrupt:
	p.stop()

GPIO.cleanup()
