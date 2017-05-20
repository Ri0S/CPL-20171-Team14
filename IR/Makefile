all : scan send

scan : scan.o
	gcc -o scan scan.o -lwiringPi

send : send.o
	gcc -lm -o send send.o -lwiringPi
	rm *.o

scan.o : scanir.c
	gcc -c -o scan.o scanir.c -lwiringPi -std=c99

send.o : sendir.c
	gcc -c -lm -o send.o sendir.c -lwiringPi -std=c99

clean :
	rm send
	rm scan
