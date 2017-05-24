import os
import sys
import subprocess
import time

while 1:
	a = subprocess.Popen(['python', '/home/pi/project/CPL-20171-Team14/fsr/read_fsr.py', sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]], stdout=subprocess.PIPE).stdout.read().strip()

	if a == "open":
		os.system("/home/pi/project/CPL-20171-Team14/takepic/takepicture")
	time.sleep(10)

