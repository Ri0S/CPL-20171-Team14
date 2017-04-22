#include <stdio.h>
#include <stdlib.h>

int main(void){
	system("fswebcam --no-banner -S 5 -r 640x480 ./pic/pic.jpg");

	return 0;
}
