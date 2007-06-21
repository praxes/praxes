#include "driver.h"

/* produce a hex dump */

void mhexdump(unsigned char *p, int len)
{
	unsigned char *line = p;
	int i, thisline, offset = 0;

	while (offset < len)
	{
		printf("%04x ", offset);
		thisline = len - offset;
		if (thisline > 16)
			thisline = 16;

		for (i = 0; i < thisline; i++)
			printf("%02x ", line[i]);

		for (; i < 16; i++)
			printf("   ");

		for (i = 0; i < thisline; i++)
			printf("%c", (line[i] >= 0x20 && line[i] < 0x7f) ? line[i] : '.');
		printf("\n");
		offset += thisline;
		line += thisline;
	}
}


int macchess_connect_motor(char *ttyDevice)
{
  int fd = open(ttyDevice, O_RDWR | O_NOCTTY | O_SYNC);
  struct termios my_termios;
  tcflush(fd, TCIFLUSH);
  my_termios.c_cflag = B38400 | CS8 |CREAD | CLOCAL | HUPCL;
  my_termios.c_lflag = NOFLSH;
  my_termios.c_iflag = 0;
  my_termios.c_oflag = 0;
  cfsetospeed(&my_termios, B38400);
  tcsetattr(fd, TCSANOW, &my_termios); 
  return fd;
}


long macchess_send_command(int fd, char command, long registerX, int writeCmd)
{
  int i, sum = 0;
  long returnreg;
  char buf[7];
  char *reg = (char *)(&registerX);
  
  buf[0] = 0xFF;
  buf[1] = command | (writeCmd << 7);
  for(i = 0; i < 4; i++)
    buf[i+2] = reg[i];
  for(i = 0; i < 6; i ++)
    sum += (int)buf[i];
  sum = 256 - (sum % 256);
  buf[6] = (char)sum;
  // mhexdump(buf, 7);
  
  write(fd, buf, 7);
  usleep(100000);
  i = read(fd, buf, 7);
  
  
  // mhexdump(buf, 7);
  returnreg = (long)buf[2];
  returnreg += (long)buf[3] << 8;
  returnreg += (long)buf[4] << 16;
  returnreg += (long)buf[5] << 24;
  return returnreg;
}


int macchess_disconnect_motor(int fd)
{
  return close(fd);
  
}


/* For testing the macchess navitar control */
/*
int main()
{
  int fd;
  long reply;
  fd = macchess_connect_motor("/dev/ttyS0");
  reply = macchess_send_command(fd,0x01,0, 0);
  printf("The register sent back is: %d\n", reply);
  reply = macchess_send_command(fd,REG_USER_LIMIT_1,0,1);
  printf("The register sent back is: %d\n", reply);
  macchess_disconnect_motor(fd);
}
*/
