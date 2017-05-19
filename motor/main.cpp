#include <stdio.h>
#include <wiringPi.h>
#include <softPwm.h>

#define SERVO 1

int main(void){
	wiringPiSetup();

	softPwmCreate(SERVO, 0, 300);

	while(1)
		softPwmWrite(SERVO, 24);

	return 0;
}
