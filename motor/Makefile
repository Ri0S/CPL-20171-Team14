servo : main.o
	gcc -o servo main.o -lwiringPi
	rm *.o

main.o : main.cpp
	gcc -c -o main.o main.cpp -lwiringPi

clean:
	rm servo
