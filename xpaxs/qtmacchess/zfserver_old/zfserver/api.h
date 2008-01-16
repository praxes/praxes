#include "driver.h"
#ifndef API_H
#define API_H

void initMotors(char *ttyName);
void  moveMotor(int motor, long where);
int motorRange(int motor);
int motorCurrent(int motor);
void disconnectMotors();

#endif
