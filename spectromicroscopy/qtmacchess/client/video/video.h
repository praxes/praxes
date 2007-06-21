  /*-----------------------------------------------------------------------
   *  MACCHESS 1394 Camera Communication module
   *-----------------------------------------------------------------------*/

#ifndef CONVERSIONS_H
#define CONVERSIONS_H

int  macchess_initialize_client(char *ipAddr, int port);
void macchess_get_decompressed_frame(unsigned char *buf);
void macchess_close_connection();
void macchess_send_kill();
void macchess_send_crosshairs(int crossX, int crossY);
#endif
