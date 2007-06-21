#include "zfthread.h"
#include "qprocess.h"
#include "unistd.h"
#include <X11/Xos.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>

ZFThread :: ZFThread()
{
    sig = new QSignal();
}

int ZFThread :: connectZoomFocus(char *ipAddr, int port)
{
  int i;
  zfsocket_fd = socket(AF_INET,SOCK_STREAM,0);
  // printf("socket returned: %d\n",zfsocket_fd);
  serv.sin_family=AF_INET;
  inet_aton(ipAddr,&(serv.sin_addr));
  // printf("127.0.0.1 is really: %d\n",serv.sin_addr);
  // REG!! another hard-coded value
 
//  F1 setup 
//  serv.sin_port=htons(4001);
  
// F2 setup
   serv.sin_port=htons(port);
  
  i = connect(zfsocket_fd,(struct sockaddr *)&serv, sizeof(serv));
  // printf("Connect returned: %d\n",i);
  return i;
}

void ZFThread :: sigConnect( QObject *receiver, const char *member)
{
    sig->connect( receiver, member );
 }

long ZFThread :: send_command(char cmd, long inReg)
{
    long reg =0;
    int i = 0;

    switch(cmd & 0xf)
    {
    case 0x1:
    case 0x2:
	mutex.lock();
	write(zfsocket_fd, &cmd, 1);
	//printf("Wrote motor range request %2X\n",cmd);
	i = read(zfsocket_fd,&reg,4);
	//printf("Read %d bytes, Got motor range response %d\n",i,reg);
	mutex.unlock();
	break;
    case 0x3:
	mutex.lock();
	//fprintf(stderr, "Move Request Locked Mutex\n");
	write(zfsocket_fd, &cmd, 1);
	write(zfsocket_fd,&inReg,4);
	//fprintf(stderr, "Moved the motor to %d\n", inReg);
	mutex.unlock();
	//fprintf(stderr, "Move Request UnLocked Mutex\n");
	break;
    case 0x4:
	mutex.lock();
	write(zfsocket_fd, &cmd, 1); 
	close(zfsocket_fd);
	zfsocket_fd = -1;
	DataSource :: connectedToZoomFocus = false;
	mutex.unlock();
	break;
    default:
	break;
    }
    return reg;
}

void ZFThread :: run()
{
    long reg;
    char cmd;
    while(DataSource :: connectedToZoomFocus)
    {	
	// We need some downtime, the motors can't respond
	// too quickly.
	usleep(250000);
	mutex.lock();
	//fprintf(stderr, "Thread Locked Mutex\n");
	cmd = 0x02;
	write(zfsocket_fd, &cmd, 1);
	read(zfsocket_fd,&reg,4);
	
	// convert zoom parameter from navitar to pixels/micron 
	// was obtained by fitting actual measured data on camera
	
	//	DataSource :: pixPerMicron = exp(9.10281e-5*reg-1.28814);
	
	DataSource :: pixPerMicron = exp(DataSource::zoomSlope*reg +
					 DataSource::zoomIntercept);
	
	// HACK - to refresh crosshairs
      	if(reg + 50 < DataSource :: zoomCurrent || reg -50 > DataSource :: zoomCurrent)
	{
	  Visual visual;
	  XSetWindowAttributes xswa;
	  Display *dpy;
	  unsigned long mask = 0;
	  int screen;
	  Window win;
	  if ((dpy = XOpenDisplay(NULL)) == NULL) {
	    fprintf (stderr, "unable to open display\n");
	    return;
	  }
	  screen = DefaultScreen (dpy);
	  xswa.background_pixmap = ParentRelative;
	  
	  mask |= CWBackPixmap;
	  xswa.override_redirect = True;
	  xswa.backing_store = NotUseful;
	  xswa.save_under = False;
	  mask |= (CWOverrideRedirect | CWBackingStore | CWSaveUnder);
	  visual.visualid = CopyFromParent;
	  win = XCreateWindow(dpy, DefaultRootWindow(dpy), 400, 600, 1, 1,
			      0, DefaultDepth(dpy, screen), InputOutput, &visual, mask, &xswa);
	  XMapWindow (dpy, win);
	  /* the following will free the color that we might have allocateded */
	  XCloseDisplay (dpy);
	}
	DataSource :: zoomCurrent = reg;
	
	cmd = 0x12;
	write(zfsocket_fd, &cmd, 1);
	read(zfsocket_fd,&reg,4);
	DataSource :: focusCurrent = reg;
	//fprintf(stderr, "Thread UnLocked Mutex\n");
	mutex.unlock();
	sig -> activate();
    }
    return;
}

