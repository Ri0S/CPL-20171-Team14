#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <sys/time.h>

int readable = 1;
int read_pin = 27;
int interval = 10;
int max_wait = 40000;

void signalCallBackHandler(int sig)
{
	readable = 0;
}

double getMoment()
{
	struct timeval tv;
	gettimeofday(&tv, NULL);
	return ((double)(tv.tv_sec) * 1000000 + (double)(tv.tv_usec));
}

int main(int argc, char *argv[])
{
	int result;

	FILE *fp;
	char *fileName = "irdata.txt";
	if (argc >= 2) { fileName = argv[1]; }
	if ((fp = fopen(fileName, "w")) == NULL) {
		printf("can't open file : %s\n", fileName);
		exit(1);
	}
	printf("write file: %s\n", fileName);

	if (signal(SIGINT, signalCallBackHandler) == SIG_ERR) {
		printf("can't set signal\n");
		exit(1);
	}

	if (wiringPiSetup() == -1) {
		printf("error wiringPi setup\n");
		exit(1);
	}

	if (argc >= 3) {
		read_pin = atoi(argv[2]);
	}
	pinMode(read_pin, INPUT);
	printf("scaning pin: %d (wiringpi)\n", read_pin);

	if (argc >= 4) {
		max_wait = atoi(argv[3]) * 1000;
	}
	printf("max keep time: %d(ms)\n", max_wait / 1000);

	printf("Infrared LED scanning start.\n");
	printf("Pressed Ctrl+C, this program will exit.\n");

	result = scan(fp);

	fclose(fp);

	if (result || !readable) {
		printf("\n\n!!! could not scanning. quit.\n\n");
	}
	else {
		printf("\nScanning has been done.\n\n");
	}

	return 0;
}

int scan(FILE *fp) {
	if (!digitalRead(read_pin)) { return 1; }

	int on, off;

	while (readable && digitalRead(read_pin)) {}

	while (readable) {
		on = getTime(0);
		off = getTime(1);
		fprintf(fp, "%6d %6d\n", on, off);

		if (off > max_wait) { break; }
	}

	return 0;
}

int getTime(int status) {
	int count = 0;
	int max = max_wait / interval;
	double start, end;

	start = getMoment();
	while (digitalRead(read_pin) == status) {
		delayMicroseconds(interval);
		count++;
		if (count > max) { break; }
	}
	end = getMoment();

	return getInterval(start, end);
}

int getInterval(double t1, double t2) {
	return (int)(t2 - t1);
}
