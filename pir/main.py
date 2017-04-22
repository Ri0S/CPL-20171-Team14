import RPi.GPIO as GPIO
import time

PINOUT = 14
PININ = 15

GPIO.setmode(GPIO.BCM)
GPIO.setup(PININ, GPIO.IN)
GPIO.setup(PINOUT, GPIO.OUT)

def pir(channel):
	GPIO.output(14, GPIO.LOW)
	if GPIO.input(channel) == 1:
		global counter
		GPIO.output(PINOUT, GPIO.HIGH)
		print("Motion detected")


GPIO.add_event_detect(PININ, GPIO.BOTH, callback=pir, bouncetime=150)

try:
	while True:
		time.sleep(0.5)

except KeyboardInterrupt:
	print("Inturrupt")

finally:
	GPIO.cleanup()
