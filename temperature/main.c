#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define MAXTIMINGS 85

int dht11_dat[5] = {0,};
int PININ = 15;

void read_temp(){
	uint8_t laststate = HIGH;
	uint8_t counter = 0;
	uint8_t j = 0;
	float f;

	for(int i = 0; i < 5; i++)
		dht11_dat[i] = 0;
	
	pinMode(PININ, OUTPUT);
	digitalWrite(PININ, LOW);
	delay(18);
	digitalWrite(PININ, HIGH);
	delayMicroseconds(40);

	pinMode(PININ, INPUT);

	for(int i = 0; i < MAXTIMINGS; i++){
		counter = 0;
		while(digitalRead(PININ) == laststate){
			counter++;
			delayMicroseconds(1);
			if(counter == 255)
				break;
		}
		laststate = digitalRead(PININ);
		
		if(counter == 255)
			break;

		if((i>=4) && (i%2 == 0)){
			dht11_dat[j/8] <<= 1;
			if(counter > 16)
				dht11_dat[j/8] |= 1;
			j++;
		}
	}

	if((j >=40) && (dht11_dat[4] == (dht11_dat[0] + dht11_dat[1] + dht11_dat[2] + dht11_dat[3]))){
		printf("Humidity = %d.%d, Temperature = %d.%d C\n", dht11_dat[0], dht11_dat[1], dht11_dat[2], dht11_dat[3]);
	} 
}

int main(int argc, char **argv){
	PININ = atoi(argv[1]);
	if(wiringPiSetup() == -1)
		exit(1);
	
	for(int i = 0; i<5000; i++){
		read_temp();
		delay(200);
	}
	return 0;
}
