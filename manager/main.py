from socket import*
import subprocess
import os

BUFSIZE = 1024

automode = [[0],[],[]]
###########################################
PINSET_MODE = 0
MODESET_MODE = 1
DOORSET_MODE = 2
REQUEST = 3
###########################################
FSR_SPICLF = []
FSR_SPIMISO = []
FSR_SPIMOSI = []
FSR_SPICS = []

TEMP_PININ = []

PIR_PININ = []
PIR_PINOUT = []

IR_PINOUT = []

MOTOR_PINOUT = []

LED_PINOUT = []
###########################################
def pin_update():
	f = open("pindb", "r")
	del FSR_SPICLF[:]
	del FSR_SPIMISO[:]
	del FSR_SPIMOSI[:]
	del FSR_SPICS[:]
	del TEMP_PININ[:]
	del PIR_PININ[:]
	del PIR_PINOUT[:]
	del IR_PINOUT[:]
	del MOTOR_PINOUT[:]
	del LED_PINOUT[:]
	
	del automode[1][:]
	del automode[2][:]

	while 1:
		strr = f.readline()
		if strr == '':
			break
		if strr[0:2] == "IR":
                        IR_PINOUT.append(int(f.readline()))
		elif strr[0:3] == "FSR":
			FSR_SPICLF.append(int(f.readline()))
			FSR_SPIMISO.append(int(f.readline()))
			FSR_SPIMOSI.append(int(f.readline()))
			FSR_SPICS.append(int(f.readline()))
			automode[1].append(0)
		elif strr[0:3] == "PIR":
			PIR_PININ.append(int(f.readline()))
			PIR_PINOUT.append(int(f.readline()))
			automode[2].append(0)
		elif strr[0:3] == "LED":
			LED_PINOUT.append(int(f.readline()))
		elif strr[0:4] == "TEMP":
                        TEMP_PININ.append(int(f.readline()))
		elif strr[0:5] == "MOTOR":
			MOTOR_PINOUT.append(int(f.readline()))
	f.close()

def pin_file_update():
	f = open("pindb", "w")
	
	i = 0
	for t in PIR_PININ:
		f.write("PIR" + str(i) + "\n")
		f.write("\t" + str(PIR_PININ[i]) + "\n" + 
			"\t" + str(PIR_PINOUT[i]) + "\n")
		i+=1
	i = 0
	for t in FSR_SPICLF:
		f.write("FSR" + str(i) + "\n")
		f.write("\t" + str(FSR_SPICLF[i]) + "\n" + 
			"\t" + str(FSR_SPIMISO[i]) + "\n" +
			"\t" + str(FSR_SPIMOSI[i]) + "\n" +
			"\t" + str(FSR_SPICS[i]) + "\n")
		i+=1
	i = 0
	for t in TEMP_PININ:
		f.write("TEMP" + str(i) + "\n")
		f.write("\t" + str(TEMP_PININ[i]) + "\n")
		i+=1
	i = 0
	for t in IR_PINOUT:
		f.write("IR" + str(i) + "\n")
		f.write("\t" + str(IR_PINOUT[i]) + "\n")
 		i+=1
	i = 0
	for t in LED_PINOUT:
		f.write("LED" + str(i) + "\n")
		f.write("\t" + str(LED_PINOUT[i]) + "\n")
		i+=1
	i = 0
	for t in MOTOR_PINOUT:
		f.write("MOTOR" + str(i) + "\n")
		f.write('\t' + str(MOTOR_PINOUT[i]) + '\n')
		i +=1

	f.close()
	

def pin_set(device, devicenum, pin):
	if device == 0:
		if len(PIR_PININ) < devicenum+1:
			PIR_PININ.append(pin[0])
			PIR_PINOUT.append(pin[1])
		else:
			PIR_PININ[devicenum] = pin[0]
			PIR_PINOUT[devicenum] = pin[1]
	elif device == 1:
		if len(FSR_SPICLF) < devicenum+1:
			FSR_SPICLF.append(pin[0])
			FSR_SPIMISO.append(pin[1])
			FSR_SPIMOSI.append(pin[2])
			FSR_SPICS.append(pin[3])
		else:
			FSR_SPICLF[devicenum] = pin[0]
			FSR_SPIMISO[devicenum] = pin[1]
			FSR_SPIMOSI[devicenum] = pin[2]
			FSR_SPICS[devicenum] = pin[3]

	elif device == 2:
		if len(TEMP_PININ) < devicenum+1:
			TEMP_PININ.append(pin[0])
		else:
			TEMP_PININ[devicenum] = pin[0]
	elif device == 3:
		if len(IR_PINOUT) < devicenum+1:
			IR_PINOUT.append(pin[0])
		else:
			IR_PINOUT[devicenum] = pin[0]
	elif device == 4:
		if len(LED_PINOUT) < devicenum+1:
			LED_PINOUT.append(pin[0])
		else:
			LED_PINOUT[devicenum] = pin[0]
	elif device == 5:
		if len(MOTOR_PINOUT) < devicenum+1:
			MOTOR_PINOUT.append(pin[0])
		else:
			MOTOR_PINOUT[devicenum] = pin[0]
		

pin_update()

#serverName = "127.0.0.1"
#serverPort = 12345

HOST = ''
PORT = 12345

#clientSocket = socket(AF_INET, SOCK_STREAM)
#clientSocket.connect((serverName, serverPort))

s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
autopid = [[]]
while 1:
	clientSocket, addr = s.accept()
	buff = clientSocket.recv(BUFSIZE)
	print buff
	pid = os.fork()
	if pid != 0:
		clientSocket.close()
	if int(buff[0:2]) == 1 and pid != 0:
		if int(buff[6:8] == 0):
			for tt in autopid:
				if tt[0] == int(buff[2:4]) and tt[1] == int(buff[4:6]):
					os.system("kill" + str(tt[2]))
					autopid.remove(tt)
					break
		elif int(buff[6:8] == 1):
			autopid.append([int(buff[2:4]), int(buff[4:6]), pid])
	if pid == 0:
		opt = int(buff[0:2])
		if opt == 0:
			devi = int(buff[2:4])
			dn = int(buff[4:6])
			if devi == 0:
				pin = [int(buff[6:8]), int(buff[8:10])]
			elif devi == 1:
				pin = [int(buff[6:8]), int(buff[8:10]), int(buff[10:12]), int(buff[12:14])]
			elif devi == 2:
				pin = [int(buff[6:8])]
			elif devi == 3:
	                        pin = [int(buff[6:8])]
			elif devi == 4:
				pin = [int(buff[6:8])]
			elif devi == 5:
	                        pin = [int(buff[6:8])]
			
			pin_set(devi, dn, pin)
			pin_file_update()

		elif opt == 1:
			devi = int(buff[2:4])
			dn = int(buff[4:6])
			modee = int(buff[6:8])
			if modee == 1:
				if dn == 0:
					print
				elif dn == 2:
					os.system("python /home/pi/CPL-20171-Team14/pir/main.py" + ' ' + str(PIR_PININ[dn]) + ' ' + str(PIR_PINOUT[dn]) + ' ' + str(LED_PINOUT[dn]))
			
			
		elif opt == 2:
			dn = int(buff[2:4])
			os.system("python /home/pi/project/CPL-20171-Team14/fsr/set_fsr.py" + ' ' + str(SPICLK[dn]) + ' ' + str(SPIMISO[dn]) + ' ' + str(SPIMOSI[dn]) + ' ' + str(SPICS[dn]))

		elif opt == 3:
			func = int(buff[2:4])
			dn = int(buff[4:6])
			if func == 0:
				os.system("sudo rm -rf /home/pi/project/CPL-20171-Team14/IR/irdata.txt")
				irf = open("/home/pi/project/CPL-20171-Team14/IR/irdata.txt", "w")
				i = 0
				while 1:
					c =  clientSocket.recv(BUFSIZE)
					if 'end' in c:
						if i == 0:
							print "asdf" + c.split('end')[0]
							irf.write(c.split('end')[0])
						print "break"
						break
					irf.write(c)
					i+=1
				irf.close()			
	
				os.system("/home/pi/project/CPL-20171-Team14/IR/send /home/pi/project/CPL-20171-Team14/IR/irdata.txt 3 " + str(IR_PINOUT[dn]))
				print "/home/pi/project/CPL-20171-Team14/IR/send irdata.txt 3 " + str(IR_PINOUT[dn])
			if func == 1:
				a = subprocess.Popen(['python', '/home/pi/project/CPL-20171-Team14/fsr/read_fsr.py', str(SPICLK[dn]), str(SPIMISO[dn]), str(SPIMOSI[dn]), str(SPICS[dn])], stdout=subprocess.PIPE).stdout.read().strip()
				if a == "open":
					clientSocket.send("1")
				elif a == "close":
					clientSocket.send("0")

			elif func == 2:
				os.system("/home/pi/project/CPL-20171-Team14/takepic/takepicure" + room + "pic.jpg")
				fi = open("/home/pi/project/CPL-20171-Team14/takepic/pic/" + room + "/pic.jpg")
				clientSocket.send(fi.read())

			elif func == 3:
				onoff = int(buff[6:8])
				os.system("python /home/pi/project/CPL-20171-Team14/led/main.py" + str(LED_PINOUT[dn]) + str(onoff)) 
		clientSocket.send("1")	
		clientSocket.close()
	

