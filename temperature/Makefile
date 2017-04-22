temperature : main.o
	gcc -o temperature main.o -lwiringPi
	rm *.o

main.o : main.c
	gcc -c -o main.o main.c -lwiringPi -std=c99

clean :
	rm temperature
