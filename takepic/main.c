#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv){
	char buf[512];
	sprintf(buf, "fswebcam --no-banner -S 5 -r 640x480 /home/pi/project/CPL-20171-Team14/takepic/pic/%s", argv[1]);
	system(buf);

	return 0;
}
