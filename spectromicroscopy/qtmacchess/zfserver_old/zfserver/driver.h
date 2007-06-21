#ifndef DRIVER_H
#define DRIVER_H
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <termios.h>
#include "rs232.h"



int macchess_connect_motor(char *ttyDevice);
long macchess_send_command(int fd, char command, long registerX, int writeCmd);
int macchess_disconnect_motor(int fd);

#endif
