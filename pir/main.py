import RPi.GPIO as GPIO
import time
import os
import socket
import sys

room = "room1"

wtob = [17, 18, 27, 22, 23, 24, 25, 4, 2, 3, 8, 7, 10, 9, 11, 14, 15, -1, -1, -1, -1, 5, 6, 13, 19, 26, 12, 16, 20, 21, 0]

PININ = wtob[int(sys.argv[1])]
PINOUT = wtob[int(sys.argv[2])]
LED = wtob[int(sys.argv[3])]

GPIO.setmode(GPIO.BCM)
GPIO.setup(PININ, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

def pir(channel):
	if GPIO.input(channel) == 1:
		global counter
		GPIO.output(LED, GPIO.HIGH)
		print("Motion detected")

GPIO.add_event_detect(PININ, GPIO.BOTH, callback=pir, bouncetime=150)

try:
	while True:
		time.sleep(0.2)


except KeyboardInterrupt:
	print("Inturrupt")

finally:
	GPIO.cleanup()
