import subprocess
import os
import sys
import time

while 1:
	a = subprocess.Popen(['python', '/home/pi/project/CPL-20171-Team14/light/main.py'], stdout=subprocess.PIPE).stdout.read().strip()
	if float(a) > 200:
		os.system("/home/pi/project/CPL-20171-Team14/motor/servo " + sys.argv[1] + " 0")
	else:
		os.system("/home/pi/project/CPL-20171-Team14/motor/servo " + sys.argv[1] + " 1")
	
	time.sleep(10)
