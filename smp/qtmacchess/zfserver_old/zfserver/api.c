#include "driver.h"
#include "api.h"
int fd;

void initMotors(char *ttyName)
{
  fd = macchess_connect_motor(ttyName);
}

void  moveMotor(int motor, long where)
{
  char command = motor ? REG_USER_TARGET_2 : REG_USER_TARGET_1;
  macchess_send_command(fd, command, (long)where, 1);   
}

int motorRange(int motor)
{
  char command = motor ? REG_SETUP_LIMIT_2 : REG_SETUP_LIMIT_1;
  return macchess_send_command(fd, command, 0, 0);   
}

int motorCurrent(int motor)
{
  char command = motor ? REG_USER_CURRENT_2 : REG_USER_CURRENT_1;
  return macchess_send_command(fd, command, 0, 0);   
}

void disconnectMotors()
{
  macchess_disconnect_motor(fd);
}
