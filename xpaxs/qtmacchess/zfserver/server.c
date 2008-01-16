#include <ctype.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <signal.h>
#include "api.h"
int socket_fd;

void cleanup()
{
  disconnectMotors();
  close(socket_fd);
  exit(0);
}


int subserver()
{
  char cmd;
  long reg = 5000;
  int bytes_read;
  while(1)
    {
      bytes_read = read(socket_fd,&cmd,sizeof(char));
      switch(cmd & 0xf)
	{
	case 0x1: // client wants motor range
	  reg = motorRange(cmd >> 4);
	  fprintf(stderr, "Client wants motor range, sending %d\n",(int)reg);
	  write(socket_fd,&reg,sizeof(long));
	  break;
	case 0x2: // client wants current motor position
	  reg = motorCurrent(cmd >> 4);
	  write(socket_fd,&reg,sizeof(long));
	  break;
	case 0x3: // client wants to move motor
	  bytes_read = read(socket_fd,&reg,sizeof(long));
	  moveMotor(cmd >> 4, reg);
	  break;
	case 0x4: // client is finished
	  close(socket_fd);
	  return 0;
	default: fprintf(stderr, "Invalid Code Sent to Server\n");
	}
    }
  close(socket_fd);
  exit(0);
  return 0;
}


int main()
{
  int socket_id; // , socket_fd;
  struct sockaddr_in serv;
  int len;
  int i;
  long reg;
  char cmd;
  signal(SIGPIPE, cleanup);
   initMotors("/dev/ttyS0");
  //  initMotors("/dev/ttyS3");


  printf("A quick motor check:\n");
  cmd = 0x01;
  reg = motorRange(cmd >> 4);
  printf("Motor %d's range is: %d\n", (cmd >> 4) + 1, (int)reg);
  cmd = 0x11;
  reg = 0;
  reg = motorRange(cmd >> 4);
  printf("Motor %d's range is: %d\n", (cmd >> 4) + 1,(int)reg);



  socket_id = socket(AF_INET,SOCK_STREAM,0);
  printf("socket returned: %d\n",socket_id);

  serv.sin_family=AF_INET;
  serv.sin_addr.s_addr=INADDR_ANY;
  serv.sin_port=htons(4005);
  i = bind(socket_id,(struct sockaddr *)&serv,sizeof(serv));
  printf("Bind returned %d\n",i);

  i = listen(socket_id,1);
  printf("Listen returned: %d\n",i);

  while (1)
    {
      printf("About to accept a connection\n");
      len = sizeof(serv);
      socket_fd = accept(socket_id,(struct sockaddr *)&serv,&len);
      printf("Accepted a client with fd = %d\n",socket_fd);
      printf("Forking off the subserver\n");
      // i = fork();
      //if (i==0)
      //{
	  subserver();
	  //  exit(0);
	  //}
	  //else
	  //{
	  close(socket_fd);
	  //}      
    }
  disconnectMotors();
  return 0;
}
