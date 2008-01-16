  /*-----------------------------------------------------------------------
   *  MACCHESS 1394 Camera Communication module
   *-----------------------------------------------------------------------*/

#ifndef DRIVER_H
#define DRIVER_H


void macchess_initialize_camera();
unsigned char *macchess_get_raw_frame(); // unsigned char *buf);
void macchess_stop_transmission();


#endif
