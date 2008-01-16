extern "C" 
{
  #include "video.h"
}
#include <qthread.h>
#include <qsocket.h>
#include <qserversocket.h>
#include <qptrlist.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/extensions/Xvlib.h>
#include <X11/keysym.h>
// #include <videoserver.h>
#include <qsocketdevice.h>
#include <qsignal.h>
#include <qvariant.h>
#include <qmutex.h>
#ifndef XV_UYVY
#define XV_UYVY 0x59565955
#endif


#ifndef VIDEO_RENDERER_H
#define VIDEO_RENDERER_H


class VideoRenderer : public QThread
{
public:
    VideoRenderer(WId wid, QSocketDevice *socket, QMutex *mutex);
    void run();
    void stop();
    void connect( QObject *receiver, const char *member);
    int crossX; 
    int crossY;
    bool newCrossHair;
    bool broadcast;
    int keyframe;
    int newClient();
    //VideoServer *vs;
    double time;
    long size;
private:
    unsigned char buf[1024*768*2];
    unsigned char *raw;
    void toggleSocket();
    QMutex *mutex;
    
    Display *display;
    Window window;
    XGCValues xgcv;
    GC gc;
    XvImage *xv_image;
    XvAdaptorInfo *info;
    QSignal *sig;
    QSocketDevice *socket;
signals:
    
};

#endif
