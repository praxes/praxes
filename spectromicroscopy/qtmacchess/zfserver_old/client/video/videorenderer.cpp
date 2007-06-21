#include "videorenderer.h"
#include "../datasource.h"

#define YUV2RGB(y, u, v, r, g, b)\
  r = y + ((v*1436) >>10);\
  g = y - ((u*352 + v*731) >> 10);\
  b = y + ((u*1814) >> 10);\
  r = r < 0 ? 0 : r;\
  g = g < 0 ? 0 : g;\
  b = b < 0 ? 0 : b;\
  r = r > 255 ? 255 : r;\
  g = g > 255 ? 255 : g;\
  b = b > 255 ? 255 : b
      
      
void uyvy2rgb (unsigned char *src, unsigned char *dest, unsigned long long int NumPixels)
{
  register int i = (NumPixels << 1)-1;
  register int j = NumPixels + ( NumPixels << 1 ) -1;
  register int y0, y1, u, v;
  register int r, g, b;
                                                                                
  while (i > 0) {
    y1 = (unsigned char) src[i--];
    v  = (unsigned char) src[i--] - 128;
    y0 = (unsigned char) src[i--];
    u  = (unsigned char) src[i--] - 128;
    YUV2RGB (y1, u, v, r, g, b);
    dest[j--] = b;
    dest[j--] = g;
    dest[j--] = r;
    YUV2RGB (y0, u, v, r, g, b);
    dest[j--] = b;
    dest[j--] = g;
    dest[j--] = r;
  }
}



VideoRenderer :: VideoRenderer(WId wid)
{
    unsigned int num_adaptors;
    display=XOpenDisplay(getenv("DISPLAY"));
    id=Imlib_init(display);
    XvQueryAdaptors(display, DefaultRootWindow(display), &num_adaptors, &info);
    window = (Window)wid;
    XMapWindow(display,window);
    gc=XCreateGC(display,window,0,&xgcv);
    XSetForeground(display, gc, WhitePixel(display, DefaultScreen(display)));

    saveImage = false;
    zoomFactor = 1.0;
    // midpoint tool

    
} 
int VideoRenderer :: tryConnect()
{
    return macchess_initialize_client();
}

void VideoRenderer :: run()
{
   //if(macchess_initialize_client() == 0);
   //else return;

   while(true)
    {
	macchess_get_decompressed_frame(buf);
	xv_image=XvCreateImage(display,info[0].base_id, XV_UYVY, (char*)buf, 1024, 768);
	XvPutImage(display, info[0].base_id, window, gc, xv_image,
		   0,0,1024,768, 
		   0,0, 1024,768);
	
	if(DataSource :: crossHairDisplayed)
	{	
	    // Draw Horizontal CrossHair
	    XDrawLine(display, window, gc, 
		      0,   (int)(DataSource::pixPerMicron*DataSource :: crossY + DataSource::zcenY),
		      1024,(int)(DataSource::pixPerMicron*DataSource :: crossY + DataSource::zcenY));
	    // Draw Vertical CrossHair
	    XDrawLine(display, window, gc, 
		      (int)(DataSource::pixPerMicron*DataSource :: crossX + DataSource::zcenX), 0, 
		      (int)(DataSource::pixPerMicron*DataSource :: crossX + DataSource::zcenX) , 768);
	    
// Draw some tick marks	    
	    
	    for (int i=-40; i<50; i+=10) {
	    
		XDrawLine(display,window,gc,
		      (int)(DataSource::pixPerMicron*(DataSource :: crossX+i) + DataSource::zcenX), 
		      (int)(DataSource::pixPerMicron*DataSource :: crossY + DataSource::zcenY)+3, 
		      (int)(DataSource::pixPerMicron*(DataSource :: crossX+i) + DataSource::zcenX),
		      (int)(DataSource::pixPerMicron*DataSource :: crossY + DataSource::zcenY)-3);
		
	            XDrawLine(display,window,gc,
		      (int)(DataSource::pixPerMicron*(DataSource :: crossX) + DataSource::zcenX)+3, 
		      (int)(DataSource::pixPerMicron*(DataSource :: crossY+i) + DataSource::zcenY), 
		      (int)(DataSource::pixPerMicron*(DataSource :: crossX) + DataSource::zcenX)-3,
		      (int)(DataSource::pixPerMicron*(DataSource :: crossY+i) + DataSource::zcenY));
		      
	}
	    // draw a circle at the beam position
	    
	    XDrawArc(display, window, gc, 
		     (int)(DataSource::pixPerMicron*DataSource :: crossX + DataSource::zcenX) - 
		     (DataSource::pixPerMicron*DataSource :: beam_dia/2),
		     (int)(DataSource::pixPerMicron*DataSource :: crossY + DataSource::zcenY) - 
		     (DataSource::pixPerMicron*DataSource :: beam_dia/2),
		     DataSource::pixPerMicron*DataSource :: beam_dia,
		     DataSource::pixPerMicron*DataSource :: beam_dia,
		     0,360*64);
	}
	
	if (DataSource :: midpointTool) {
	    
	    XDrawLine(display, window, gc, 
		      DataSource::vertLineX-200, 
		      DataSource :: upperLineY, 
		      DataSource::vertLineX+200, 
		      DataSource :: upperLineY);
	    
	    XDrawLine(display, window, gc,
		      DataSource::vertLineX-200, 
		      DataSource :: lowerLineY,
		      DataSource::vertLineX+200, 
		      DataSource :: lowerLineY);
	    
	    XDrawLine(display, window, gc, 
		      DataSource::vertLineX-50, 
		      DataSource :: midLineY, 
		      DataSource::vertLineX+50, 
		      DataSource :: midLineY);
		      
                XDrawLine(display, window, gc, 
		      DataSource::vertLineX, 0, 
		      DataSource::vertLineX, 768); 
	}

	
	if(saveImage)
	{
		ImlibImage *im;
		int width = DataSource :: resolution;
		int height = (width * 3) / 4;
		unsigned char *rgbData = (unsigned char *)malloc(width * height *3);
                uyvy2rgb(buf, rgbData, width * height);
		im = Imlib_create_image_from_data(id, rgbData, NULL, width, height);
                if (im != NULL) {
                  Imlib_save_image(id, im, "snapshot.jpg", NULL);
		  saveImage = false;
                  Imlib_kill_image(id, im);
                }
                else {
                  fprintf(stderr, "Can't create image!");
		  saveImage = false;
                }
	    }
/*
	if(DataSource :: zoomBox)
	{
		int ax = ((-355)/(DataSource :: zoomLimit) * 
			 (DataSource :: zoomCurrent)) + 355;
		int ay = 
		int 
		XDrawRectangle(display, window, gc, ax, ay, bx - ax, by - ay)
	}
		*/
	
	// display a bar of known length 
	
	if (DataSource :: barDisplayed) {
	    
	  int barlen = (int) (100*DataSource::pixPerMicron);
	 
	XDrawRectangle(display,window,gc,25,730,barlen,10);	 
	XDrawString(display, window, gc,20+barlen/2, 760,"100 microns\n",11); 
	 
	}
    }
}

void VideoRenderer :: stop()
{
    // Can't stop segfaults with this function!
    // macchess_close_connection();
    macchess_send_kill();
    // Can't clean up yet, the GUI is still running!
    // XUnmapWindow(display,window);
    // XFlush(display);
}
