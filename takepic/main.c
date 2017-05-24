#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv){
	char buf[512];
	
	if (argc == 1)
		sprintf(buf, "fswebcam --no-banner -S 5 -r 640x480 /home/pi/project/CPL-20171-Team14/takepic/pic/pic");

	else
		sprintf(buf, "fswebcam --no-banner -S 5 -r 640x480 /home/pi/project/CPL-20171-Team14/takepic/pic/ips/pic");

	system(buf);

	return 0;
}
