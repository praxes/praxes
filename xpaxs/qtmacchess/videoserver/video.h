  /*-----------------------------------------------------------------------
   *  MACCHESS 1394 XVID Compressor Communication module
   *-----------------------------------------------------------------------*/

#ifndef VIDEO_H
#define VIDEO_H


int macchess_initialize_compressor();
unsigned char *macchess_get_frame(unsigned char *mp4_buffer, long *size, int keyframe, double *time);
void macchess_stop_compressor();


#endif
