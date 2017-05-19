#include <stdio.h>
#include <string.h>

int main(void){
	char buff[1024];
	FILE *fp;

	fp = popen("python /home/pi/project/CPL-20171-Team14/fsr/read_fsr.py", "r");

	fgets(buff, 1024, fp);

	printf("%s\n", buff);
	
	if(!strcmp(buff, "open"))
		return 1;
	if(!strcmp(buff, "close"))
		return 2;

	return 0;
}
	
