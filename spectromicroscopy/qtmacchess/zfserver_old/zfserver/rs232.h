/* This file includes a definition of the RS232 protocol used to 
 * communicate with the Navitar Axis Motors. The method of communication
 * is as follows:
 *
 * Sending Data to the 2 Axis Motor controller serial device:
 *
 *  7 bytes are written to the device. The first is a register id. The next
 *  four are the contents of a 32 bit register value, and the last is a 
 *  checksum.
 *
 *  Byte 0  : 0xff. This is a start of data stream flag.
 *  Byte 1  : Register id. Bit 7 is set to 1 for a write. 
 *            Bit 7 is set to0 for a read.
 *  Byte 2-5: 32 Bit Register Value or Zero for a Read
 *  Byte 6  : A checksum byte such that the 7 bytes sum to 0 (mod 256)
 *
 * Receiving Data from the 2 Axis Motor controller serial device:
 *
 *  7 bytes are read from the device. The first is 0xff - a handshake. The next
 *  four are the contents of a 32 bit register value, and the last is a 
 *  checksum.
 *
 *  Byte 0  : 0xff. This is a start of data stream flag.
 *  Byte 1  : Register id. Bit 7 is set to 0
 *  Byte 2-5: 32 Bit Register Value (low -> high byte order)
 *  Byte 6  : A checksum byte such that the 7 bytes sum to 0 (mod 256)
 *
 *  --Ismail Degani
 *    MACCHESS
 *    Friday, January 9th, 2004
 */

#ifndef RS232_H
#define RS232_H


/* Vendor and Product ID's */
#define NAVITAR_VENDOR_ID  0x1238
#define NAVITAR_PRODUCT_ID 0x4001


/* Read only registers */
#define REG_SYS_PRODUCTID 0x01 // returns 0x4001
#define REG_SYS_VERSIONHW 0x02
#define REG_SYS_VERSIONDATE 0x03
#define REG_SYS_VERSIONSW 0x04


/* System Setup Registers */
#define REG_SETUP_ACCEL_1 0x15 // sets motor 1 acceleration
#define REG_SETUP_ACCEL_2 0x25 // sets motor 2 acceleration

#define REG_SETUP_INITVELOCITY_1 0x16 // sets initial motor 1 velocity
#define REG_SETUP_INITVELOCITY_2 0x26 // sets initial motor 2 velocity

#define REG_SETUP_MAXVELOCITY_1 0x17 // sets maximum motor 1 velocity
#define REG_SETUP_MAXVELOCITY_2 0x27 // sets maximum motor 2 velocity

#define REG_SETUP_REVBACKLASH_1 0x18 // sets motor 1 reverse backlash value
#define REG_SETUP_REVBACKLASH_2 0x28 // sets motor 2 reverse backlash value

#define REG_SETUP_FWDBACKLASH_1 0x19 // sets motor 1 forward backlash value
#define REG_SETUP_FWDBACKLASH_2 0x29 // sets motor 2 forward backlash value

#define REG_SETUP_CONFIG_1 0x1B //sets motor 1 sensor configuration
#define REG_SETUP_CONFIG_2 0x2B // sets motor 2 sensor configuration

/*
Bit 0:0  near sensor is home
      1  far sensor is home

Bit 1: 0  reverse seek direct
       1  reverse seek thru home
*/


#define REG_SETUP_LIMIT_1 0x1C // returns motor 1 limit value
#define REG_SETUP_LIMIT_2 0x2C // returns motor 2 limit value


/* Normal Operation Registers */

#define REG_USER_TARGET_1 0x10 //motor 1 seek command
#define REG_USER_TARGET_2 0x20 //motor 2 seek command

#define REG_USER_INCREMENT_1 0x11 //motor 1 delta seek from current
#define REG_USER_INCREMENT_2 0x21 //motor 2 delta seek from current

#define REG_USER_CURRENT_1 0x12 //motor 1 current position
#define REG_USER_CURRENT_2 0x22 //motor 2 current position

#define REG_USER_LIMIT_1 0x13 // motor 1 limit seek command
#define REG_USER_LIMIT_2 0x23 //motor 2 limit seek command

/*
The value written drives the motor to one of the limits:

0  home motor
1  limit motor
*/


#define REG_USER_STATUS_1 0x14
#define REG_USER_STATUS_2 0x24

/*
Lower 8 bits (Bit 0 thru 7):
  0  idle
  1  driving to home
  2  coming off home
  3  driving to limit
  4  seeking forward
  5  deaccel in forward direction
  6  forward backlash (i.e. rev after overshoot)
  7  seeking reverse
  8  deaccel in reverse direction
  9  reverse backlash (i.e. forward after overshoot)
  11- forward deaccel during an abort
  12- reverse deaccel during an abort
Bit 8  motor on home sensor
Bit 9  motor on limit sensor 
*/




#endif
