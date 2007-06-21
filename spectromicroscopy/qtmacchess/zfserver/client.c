#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <string.h>

int main()
{
  int socket_fd;
  struct sockaddr_in serv;
  int len;
  char buffer[256];
  int i,n,bytes_read;
  long reg; 
  char cmd;
  socket_fd = socket(AF_INET,SOCK_STREAM,0);
  printf("socket returned: %d\n",socket_fd);
  
  serv.sin_family=AF_INET;

  inet_aton("127.0.0.1",&(serv.sin_addr));
  printf("127.0.0.1 is really: %d\n",serv.sin_addr);
  serv.sin_port=htons(4001);

  i = connect(socket_fd,(struct sockaddr *)&serv, sizeof(serv));
  printf("Connect returned: %d\n",i);

  cmd = 0x01;
  write(socket_fd, &cmd, 1);
  printf("Wrote motor range request\n",reg);
  read(socket_fd,&reg,4);
  printf("Got: %d as the motor range\n",reg);

  cmd = 0x02;
  write(socket_fd, &cmd, 1);
  read(socket_fd,&reg,4);
  printf("Got: %d as the motor current position\n",reg);

  cmd = 0x03;
  reg = 10000;
  write(socket_fd, &cmd, 1);
  write(socket_fd,&reg,4);
  printf("Moving the motor to %d\n", (int)reg);

  cmd = 0x04;
  write(socket_fd, &cmd, 1);
      //  }
  close(socket_fd);
  return 0;
}

