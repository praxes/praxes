extern "C" 
{
  #include "video.h"
  #include "conversions.h"
}
#include <qthread.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/extensions/Xvlib.h>
#include <X11/keysym.h>
#include <Imlib.h>

#include <qmutex.h>

#ifndef XV_UYVY
#define XV_UYVY 0x59565955
#endif

class VideoRenderer : public QThread
{
public:
    VideoRenderer(WId wid);
    //  VideoRenderer(WId wid, int x, int y);
    void run();
    void stop();
    int tryConnect();
    // crosshair display
    

    //bool newCrossHair;
    
    // scale display
    
    //bool barDisplayed;
    
    //int beam_dia;
    float zoomFactor;  // in pixels per micron
    bool saveImage;
    // midpoint tool
    
    //int upperLineY;
    //int lowerLineY;
    //int midLineY;
    // bool newMidpoint;
    //bool midpointTool;
    
private:
    unsigned char buf[1024*768*2];
    Display *display;
    Window window;
    XGCValues xgcv;
    GC gc;
    XvImage *xv_image;
    XvAdaptorInfo *info;
    ImlibData *id;
    QMutex mutex;
    
};
