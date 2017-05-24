#include <wiringPi.h>
#include <softPwm.h>
#include <stdio.h>

#define SERVO 4

int main(void){
	wiringPiSetup();

	softPwmCreate(SERVO, 0, 10000);

	for(int i = 0; i<300000; i++){

		softPwmWrite(SERVO, 30);
		printf("%d\n", i);
	}
	return 0;
}
