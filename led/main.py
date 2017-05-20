import RPi.GPIO as GPIO
import sys

wtob = [17, 18, 27, 22, 23, 24, 25, 4, 2, 3, 8, 7, 10, 9, 11, 14, 15, -1, -1, -1, -1, 5, 6, 13, 19, 26, 12, 16, 20, 21, 0]

GPIO.setmode(GPIO.BCM)

PINOUT = wtob[int(sys.argv[1])]
GPIO.setup(PINOUT, GPIO.OUT)

if sys.argv[2] == '0':
	GPIO.output(PINOUT, True)
elif sys.argv[2] == '1':
	GPIO.output(PINOUT, False)

