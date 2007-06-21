#include <qvariant.h>
#include "videorenderer.h"


VideoRenderer :: VideoRenderer(WId wid, QSocketDevice *socket, QMutex *mutex)
{
    unsigned int num_adaptors;
    broadcast = false;
    //vs = new VideoServer();
    this -> socket = socket;
    this -> mutex = mutex;
    display=XOpenDisplay(getenv("DISPLAY"));
    XvQueryAdaptors(display, DefaultRootWindow(display), &num_adaptors, &info);
    window = (Window)wid;
    XMapWindow(display,window);
    gc=XCreateGC(display,window,0,&xgcv);
    XSetForeground(display, gc, WhitePixel(display, DefaultScreen(display)));
    crossX = crossY = -1;
    sig= new QSignal();
} 


int VideoRenderer :: newClient()
{
    if(keyframe == 1)
    {
	keyframe = -1;
	return 1;
    }
    return -1;
}



void VideoRenderer :: run()
{
    int i;
    macchess_initialize_compressor();

    while(true)
    {
    // lock mutex
      mutex -> lock();
      raw = macchess_get_frame(buf, &size, newClient(), &time);
      if(broadcast)
      {
        i = socket -> writeBlock((const char*)(&size), (Q_ULONG)(sizeof(long)));
	// printf("Wrote size to socket, i = %d,\n", i);
        i = socket -> writeBlock((const char *)buf, (Q_ULONG)size);
      }
     // vs -> sendData(buf, size);

     /* 
      if(newCrossHair) 
	{
	  XClearWindow(display, window);
	  newCrossHair = false;
	}
	*/
      xv_image=XvCreateImage(display,info[0].base_id, XV_UYVY, (char*)raw, 1024, 768);
      XvPutImage(display, info[0].base_id, window, gc, xv_image,
		 0,0,1024,768, 
		 0,0, 1024,768);
      /*
	if(crossX > 0)
	{
	// Draw Horizontal CrossHair
	XDrawLine(display, window, gc, 0, crossY, 1024, crossY);
	// Draw Vertical CrossHair
	XDrawLine(display, window, gc, crossX, 0, crossX, 768);
	}
      */
      // unlock mutex
      mutex -> unlock();
      sig->activate();
    }
}

void VideoRenderer :: connect( QObject *receiver, const char *member)
 {
     sig->connect( receiver, member );
 }
 




void VideoRenderer :: stop()
{
  // We should never really get here
  // macchess_close_connection();
  // Also put XUnmap stuff here
}
