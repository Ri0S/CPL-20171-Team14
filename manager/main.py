from socket import*
import os

BUFSIZE = 1024
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
		elif strr[0:3] == "PIR":
			PIR_PININ.append(int(f.readline()))
			PIR_PINOUT.append(int(f.readline()))
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
	elif device == 5:
		if len(MOTOR_PINOUT) < devicenum+1:
			MOTOR_PINOUT.append(pin[0])
		else:
			MOTOR_PINOUT[devicenum] = pin[0]
		

pin_update()

serverName = "127.0.0.1"
serverPort = 12345

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName, serverPort))

while 1:
	buff = clientSocket.recv(BUFSIZE)
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
		elif devi == 5:
                        pin = [int(buff[6:8])]
		
		pin_set(0, dn, pin)
		pin_file_update()
#	elif opt == 1:
	elif opt == 2:
		os.system("python /home/pi/project/CPL-20171-Team14/fsr/set_fsr.py")
#	elif opt == 3:

clientSocket.close()

