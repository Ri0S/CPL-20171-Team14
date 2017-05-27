#include <wiringPi.h>
#include <softPwm.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int SERVO = 4;

int main(int argc, char **argv){
	SERVO = atoi(argv[1]);
	int opt = atoi(argv[2]);
	int init = time(NULL);
	wiringPiSetup();

	softPwmCreate(SERVO, 0, 10000);
	if(opt == 0){
		softPwmCreate(SERVO, 0, 10000);
		while(1){
			softPwmWrite(SERVO, 30);
			if(time(NULL) - init > 4){
				break;
			}
		}
	}
	if(opt == 1){
		softPwmCreate(SERVO, 0, 10000);
		while(1){
			softPwmWrite(SERVO, 1);
			if(time(NULL) - init > 4){
				break;
			}
		}
	}
	return 0;
}
