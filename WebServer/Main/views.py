# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from Main.models import Raspberry, Sensor
from django.urls import reverse
import socket
# Create your views here.

PIN_SETTING = "00"
MODE_SETTING = "01"
DOOR_SETTING = "02"
REQUEST = "03"
ServerPort = 12345

def RegisterRasp(request):
    if request.method == "POST":
        ip = request.POST.get('Ip',"")
        try:
            rasp = Raspberry.objects.create(Ip=ip)
            rasp.save()
            return HttpResponse("<script>alert('Register success');location.href = document.referrer;</script>")
        except:
            return HttpResponse("<script>alert('Register fail'); location.href = document.referrer;</script>")

def PinSetting(request, RpiIp):
	table_list = []
	rasp = Raspberry.objects.get(Ip=RpiIp)
	Sensorlist = Sensor.objects.filter(Ip=rasp)
	
	for sensor in Sensorlist:
		tmp = {"Name":'', "moduleNum": '', "pin":''}
		tmp["Name"] = sensor.SensorName
		tmp["moduleNum"] = str(sensor.moduleNum)
		pin_set = ''
		if sensor.Pin1 != None:
			if sensor.SensorName == "PIR":
				pin_set += "PinIn: "
			elif sensor.SensorName == "FSR":
				pin_set += "SPICLF: "
			elif sensor.SensorName == "TEMP":
				pin_set += "PinIn: "
			elif sensor.SensorName == "IR":
				pin_set += "PinOut: "
			elif sensor.SensorName == "LED":
				pin_set += "pinOut: "
			elif sensor.SensorName == "Motor":
				pin_set += "PinOut: "
			pin_set += str(sensor.Pin1)
			pin_set += " "		
		if sensor.Pin2 != None:
			if sensor.SensorName == "PIR":
				pin_set += "PinOut: "
			elif sensor.SensorName == "FSR":
				pin_set += "SPIMISO: "		
			pin_set += str(sensor.Pin2)
			pin_set += " "		
		if sensor.Pin3 != None:
			if sensor.SensorName == "FSR":
				pin_set += "SPIMOSI: "
			pin_set += str(sensor.Pin3)
			pin_set += " "		
		if sensor.Pin4 != None:
			if sensor.SensorName == "FSR":
				pin_set += "SPICS: "
			pin_set += str(sensor.Pin4)
			pin_set += " "
		tmp["pin"] = pin_set
		table_list.append(tmp)
	
	if request.method == "POST":
		SensorName = request.POST.get("Sensor", '')
		moduleNum = request.POST.get("ModuleNum", '')
		if SensorName == "Temperture":
			SensorName = "TEMP"
		
		try:
			if SensorName == "PIR":
				pin_in = request.POST.get("PinIn",'')
				pin_out = request.POST.get("PinOut",'')

				s = socket.socket()
				s.connect((RpiIp, ServerPort))

				protocol = PIN_SETTING + "00" + moduleNum.zfill(2) + pin_in.zfill(2) + pin_out.zfill(2)
				s.send(protocol)
				s.close()

				new_pin = Sensor.objects.create(Ip=rasp, SensorName=SensorName, moduleNum=moduleNum, Pin1=pin_in, Pin2=pin_out)
				new_pin.save()

			elif SensorName == "FSR":
				spiclf = request.POST.get("SPICLF",'')
				spimiso = request.POST.get("SPIMISO", '')
				spimosi = request.POST.get("SPIMOSI", '')
				spics = request.POST.get("SPICS",'')


				s = socket.socket()
				s.connect((RpiIp, ServerPort))

				protocol = PIN_SETTING + "01" + moduleNum.zfill(2) + spiclf.zfill(2) + spimiso.zfill(2) + spimosi.zfill(2) + spics.zfill(2)
				s.send(protocol)
				s.close()

				new_pin = Sensor.objects.create(Ip=rasp, SensorName=SensorName, moduleNum=moduleNum, Pin1=spiclf, Pin2=spimiso, Pin3=spimosi, Pin4=spics)
				new_pin.save()
				setUrl = reverse('DoorSetting', args=(RpiIp,))
				return HttpResponse("<a href="+setUrl+">calibration FSR link click!! </a>");
			
			elif SensorName == "TEMP":
				pin_in = request.POST.get("PinIn",'')

				s = socket.socket()
				s.connect((RpiIp, ServerPort))

				protocol = PIN_SETTING + "02" + moduleNum.zfill(2) + pin_in.zfill(2)
				s.send(protocol)
				s.close()

				new_pin = Sensor.objects.create(Ip=rasp, SensorName=SensorName, moduleNum=moduleNum, Pin1=pin_in)
				new_pin.save()

			elif SensorName == "IR" or SensorName == "LED" or SensorName == "Motor":
				pin_out = request.POST.get("PinOut", '')

				s = socket.socket()
				s.connect((RpiIp, ServerPort))

				protocol = PIN_SETTING + "02" + moduleNum.zfill(2) + pin_out.zfill(2)
				s.send(protocol)
				s.close()

				new_pin = Sensor.objects.create(Ip=rasp, SensorName=SensorName, moduleNum=moduleNum, Pin1=pin_out)
				new_pin.save()
			return HttpResponse("<script>alert('Register success');location.href = document.referrer;</script>")
		except:
			return HttpResponse("<script>alert('Register fail');location.href = document.referrer;</script>")
		
			
	return render(request, "Pinset.html", {"RpiIp":RpiIp, "Sensors":table_list})
    
def index(request):
	return render(request, 'index.html', {})

def RaspSetting(request):
	table_list = []
	rasplist = Raspberry.objects.all()
	for rpi in rasplist:
		tmp = {"Ip":'', "Ips": '', "Blind":'', "Light":'', "pin":''}
		tmp["Ip"] = rpi.Ip
		tmp["Ips"] = rpi.auto_Ips
		tmp["Blind"] = rpi.auto_Blind
		tmp["Light"] = rpi.auto_Light
		
		pin_set = ''
		Sensors = Sensor.objects.filter(Ip=rpi)
		for sensor in Sensors:
			pin_set += "[" + sensor.SensorName + "] "
			if sensor.moduleNum != None:
				pin_set += "module num: "
				pin_set += str(sensor.moduleNum)
				pin_set += "\n"

			if sensor.Pin1 != None:
				if sensor.SensorName == "PIR":
					pin_set += "PinIn: "
				elif sensor.SensorName == "FSR":
					pin_set += "SPICLF: "
				elif sensor.SensorName == "TEMP":
					pin_set += "PinIn: "
				elif sensor.SensorName == "IR":
					pin_set += "PinOut: "
				elif sensor.SensorName == "LED":
					pin_set += "PinOut: "
				elif sensor.SensorName == "Motor":
					pin_set += "PinOut: "

				pin_set += str(sensor.Pin1)
				pin_set += "\n"

			if sensor.Pin2 != None:
				if sensor.SensorName == "PIR":
					pin_set += "PinOut: "
				elif sensor.SensorName == "FSR":
					pin_set += "SPIMISO: "

				pin_set += str(sensor.Pin2)
				pin_set += "\n"

			if sensor.Pin3 != None:
				if sensor.SensorName == "FSR":
					pin_set += "SPIMOSI: "
				pin_set += str(sensor.Pin3)
				pin_set += "\n"

			if sensor.Pin4 != None:
				if sensor.SensorName == "FSR":
					pin_set += "SPICS: "
				pin_set += str(sensor.Pin4)
				pin_set += "\n"
		tmp["pin"] = pin_set
		table_list.append(tmp)
	return render(request, "raspsetting.html", {"Rpis": table_list})


def SensorRequest(request):
	Ip = '192.168.43.195'
	Port = ServerPort
	s = socket.socket()
	s.connect((Ip, Port))

	Device_Num = "00"
	'''' mode '''
	Pin_set = "00"
	Mode_set = "01"
	Door_set = "02"
	RequestMode = "03"
	''' '''

	''' Pin_setting '''
	#Pir
	PinIn = ''
	PinOut = ''
	Pir = "00" + Device_Num + PinIn + PinOut
	
	#Fsr
	SpiClf = ''
	SpiMiso = ''
	SpiMosi = ''
	Spics = ''
	FSR = "01" + Device_Num + SpiClf + SpiMiso + SpiMosi + Spics 
	
	#Temp
	tempPin = "00"
	Temp = "02" + Device_Num + tempPin
	
	''' request
	protocol =  Pin_set + Temp
	s.send(protocol)
	s.close()
	'''

	protocol = RequestMode + "01"
	s.send(protocol)

	getbuf = s.recv(1000)
	s.close()
	return HttpResponse(getbuf + "get success")

def about(request):
	return render(request, 'about.html', {})

def services(request, RpiIp):
	rasp = Raspberry.objects.get(Ip=RpiIp)
	sensor = Sensor.objects.filter(Ip=rasp)
	setList = {"BlindAuto":'', "Ips":'', "LightAuto":''}
	setList["BlindAuto"] = rasp.auto_Blind
	setList["Ips"] = rasp.auto_Ips
	setList["LightAuto"] = rasp.auto_Light

	return render(request, 'services.html', {"RpiIp":RpiIp, "Setting":setList})

def contact(request):
	return render(request, 'contact.html', {})

''' auto setting '''
def BlindAuto(request, RpiIp, On): #On: 0-> off, 1 -> on
	BLIND = "00"
	try:
		rpi = Raspberry.objects.get(Ip=RpiIp)
		sensor = Sensor.objects.get(Ip=rpi, SensorName="Motor")
		moduleNum = sensor.moduleNum
		
		s = socket.socket()
		s.connect((RpiIp, ServerPort))

		protocol = MODE_SETTING + BLIND + str(moduleNum).zfill(2) + On.zfill(2)
		s.send(protocol)
		s.close()
        
		if On == 1:
		    rpi.auto_Blind = True
		else:
		    rpi.auto_Blind = False
		rpi.save()
		return HttpResponse("success")
	except:
		return HttpResponse("fail")

def IpsAuto(request, RpiIp, On):
    IPS = "01"
    try:
        rpi = Raspberry.objects.get(Ip=RpiIp)
        sensor = Sensor.objects.get(Ip=rpi, SensorName="FSR")
        # moduleNum = sensor.moduleNum
		
        # s = socket.socket()
        # s.connect((RpiIp, ServerPort))

        # protocol = MODE_SETTING + IPS + str(moduleNum).zfill(2) + On.zfill(2)
        # s.send(protocol)
        # s.close()

        if On == "1":
            rpi.auto_Ips = True
        else:
            rpi.auto_Ips = False
        rpi.save()
        return HttpResponse("success")
    except:
        return HttpResponse("fail")

def LedAuto(request, RpiIp, On):
    LED = "02"
    try:
        rpi = Raspberry.objects.get(Ip=RpiIp)
        sensor = Sensor.objects.get(Ip=rpi, SensorName="LED")
        moduleNum = sensor.moduleNum
        
        s = socket.socket()
        s.connect((RpiIp, ServerPort))
        
        protocol = MODE_SETTING + LED + str(moduleNum).zfill(2) + On.zfill(2)
        s.send(protocol)
        s.close()

        if On == "1":
            rpi.auto_Light = True
        else:
            rpi.auto_Light = False
        rpi.save()
        return HttpResponse("success")
    except:
        return HttpResponse("fail")

def DoorSetting(request, RpiIp):
    try:
        rpi = Raspberry.objects.get(Ip=RpiIp)
        sensor = Sensor.objects.get(Ip=rpi, SensorName="FSR")

        moduleNum = sensor.moduleNum
		
        s = socket.socket()
        s.connect((RpiIp, ServerPort))

        protocol = DOOR_SETTING + str(moduleNum).zfill(2)
        s.send(protocol)
        s.close()

        return HttpResponse("success")
    except:
        return HttpResponse("fail")

''' Sensor Request '''
IR_REQUEST = "00"
DOOR_REQUEST = "01"
PIC_REQUEST = "02"
LIGHT_REQUEST = "03"
TEMP_REQUEST = "04"
def DoorCheckRequest(request, RpiIp):
	try:
		rpi = Raspberry.objects.get(Ip=RpiIp)
		sensor = Sensor.objects.get(Ip=rpi, SensorName="FSR")
		moduleNum = sensor.moduleNum
		
		s = socket.socket()
		s.connect((RpiIp, ServerPort))

		protocol = REQUEST + DOOR_REQUEST + str(moduleNum).zfill(2)
		s.send(protocol)

		response = s.recv(10)
		s.close()
		return HttpResponse("door %s" %(response))
	except:
		return HttpResponse("fail")

def LightRequest(request, RpiIp, On): #On: 1 -> on, 0 -> off
	try:
		rpi = Raspberry.objects.get(Ip=RpiIp)
		sensor = Sensor.objects.get(Ip=rpi, SensorName="LED")
		moduleNum = sensor.moduleNum
		
		s = socket.socket()
		s.connect((RpiIp, ServerPort))

		protocol = REQUEST + LIGHT_REQUEST + str(moduleNum).zfill(2) + On.zfill(2)
		s.send(protocol)
		s.close()
		return HttpResponse("success")
	except:
		return HttpResponse("fail")

def TempRequest(request, RpiIp):
	try:
		rpi = Raspberry.objects.get(Ip=RpiIp)
		sensor = Sensor.objects.get(Ip=rpi, SensorName="TEMP")
		moduleNum = sensor.moduleNum
		
		s = socket.socket()
		s.connect((RpiIp, ServerPort))

		protocol = REQUEST + TEMP_REQUEST + str(moduleNum).zfill(2)
		s.send(protocol)

		response = s.recv(10)
		s.close()
        
		response = response.split(" ")
		Humidity = response[0]
		Temp = response[1]

		return HttpResponse("Humidity: %s percent, Temp: %s" %(Humidity, Temp))
	except:
		return HttpResponse("fail")

#file send.... not yet
def IrRequest(reqeust, RpiIp, DeviceName):
	try:
		#rpi = Raspberry.objects.get(Ip=RpiIp)
		f = open("/home/pi/project/static/device/"+DeviceName, "r")
		Data = f.read()
		f.close()

		s = socket.socket()
		s.connect((RpiIp, ServerPort))

		protocol = REQUEST + IR_REQUEST + "00"
		s.send(protocol)
		s.send(Data)
		s.send("end")
		s.recv(1)
		s.close()
		return HttpResponse("success")
	except:
		return HttpResponse("fail")

def CameraRequest(request, RpiIp):
	try:
		rpi = Raspberry.objects.get(Ip=RpiIp)

		s = socket.socket()
		s.connect((RpiIp, ServerPort))

		f = open("/home/pi/project/static/Chapture.jpg", "wb")
		protocol = REQUEST + PIC_REQUEST +"00" + "00"
		s.send(protocol)
		imgBuf = ''
		# import pdb
		# pdb.set_trace()
		while 1:
			data = s.recv(20000)
			if data == "":
				break
			f.write(data)
		
		f.close()
		s.close()

		f = open("/home/pi/project/static/Chapture.jpg", "r")
		buf = f.read()
		f.close()
		return HttpResponse(buf, content_type="image/jpeg")
	except:
		return HttpResponse("fail")


def IpsBack(request, RpiIp):
    try:
        rpi = Raspberry.objects.get(Ip=RpiIp)
        sensor = Sensor.objects.get(Ip=rpi, SensorName="FSR")
        moduleNum = sensor.moduleNum
        
        s = socket.socket()
        s.connect((RpiIp, ServerPort))
        
        protocol = REQUEST + DOOR_REQUEST + str(moduleNum).zfill(2)
        s.send(protocol)
        
        response = s.recv(10)
        s.close()

        #open door
        if response == "1":
            sensor = Sensor.objects.get(Ip=rpi, SensorName="PIC")
            moduleNum = sensor.moduleNum
            
            s = socket.socket()
            s.connect((RpiIp, ServerPort))

            protocol = REQUEST + PIC_REQUEST +str(moduleNum).zfill(2) + "00"
            s.send(protocol)
        
            imgBuf = ''
            while True:
                imgBuf += s.recv(1)
                if "\xff\xd9" in imgBuf:
                        break
            return HttpResponse(imgBuf, content_type="image/jpeg")
        else:
            return HttpResponse("closed")

    except:
        return HttpResponse("fail")