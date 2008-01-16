OBJECTS = driver.o api.o server.o
CFLAGS = -O3 -Wall 

zfserver: $(OBJECTS)
	$(CC) $(CFLAGS) $(OBJECTS) -o zfserver
driver.o: driver.c driver.h
	$(CC) $(CFLAGS) -c driver.c
conversions.o: api.c api.h
	$(CC) $(CFLAGS) -c conversions.c
server.o: server.c
	$(CC) $(CFLAGS) -c server.c
clean:
	rm -f *.o *~ *# zfserver
