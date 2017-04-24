import RPi.GPIO as GPIO
import time
import os
import socket

PINOUT = 14
PININ = 15
room = "room1"
GPIO.setmode(GPIO.BCM)
GPIO.setup(PININ, GPIO.IN)
GPIO.setup(PINOUT, GPIO.OUT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.43.199', 10002))

def pir(channel):
	GPIO.output(14, GPIO.LOW)
	if GPIO.input(channel) == 1:
		global counter
		GPIO.output(PINOUT, GPIO.HIGH)
		os.system("/home/pi/project/CPL-20171-Team14/takepic/takepicture " + room + "/pic.jpg")
		print("Motion detected")
		fi = open("/home/pi/project/CPL-20171-Team14/takepic/pic/" + room + "/pic.jpg")
		s.send(fi.read())

GPIO.add_event_detect(PININ, GPIO.BOTH, callback=pir, bouncetime=2000)

try:
	while True:
		time.sleep(0.2)


except KeyboardInterrupt:
	print("Inturrupt")

finally:
	GPIO.cleanup()
