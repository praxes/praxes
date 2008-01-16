void VideoWidget :: init()
{
    vw  = new VideoRenderer(this -> winId());
     // vw -> start();
    
   // initial values for midpoint tool  



 }


void VideoWidget :: saveImage()
{
    vw -> saveImage = true;
}


void VideoWidget :: destroy()
{
}

void VideoWidget :: start()
{
    if(vw -> tryConnect() == 0)
    {
	emit videoConnected();
	vw -> start();
    }
    else fprintf(stderr, "Something is wrong with the video Stream");
}

void VideoWidget :: stop()
{
    vw -> stop();
}



void VideoWidget::setCrossHair( int x, int y )
{
    DataSource :: crossX = x;
    DataSource :: crossY = y;
}

void VideoWidget::mouseDoubleClickEvent ( QMouseEvent * e )
{
    if(DataSource :: crossHairEnabled)
    {
	DataSource :: crossX = (e -> x() - DataSource::zcenX)/DataSource::pixPerMicron;
	DataSource :: crossY = (e -> y() - DataSource::zcenY)/DataSource::pixPerMicron;
	
	DataSource :: save();
	
	// sleep(1);
	//repaint(false);
	// DataSource :: newCrossHair = true;
    }
    
    // update the nearest horizaontal line if midpoint tool is in effect
    if(DataSource :: midpointToolEnabled)
    {
	
	DataSource::lowerLineY = DataSource::upperLineY;
	DataSource::upperLineY = e->y();
	
	DataSource :: midLineY = 
		(int)((DataSource :: upperLineY + DataSource :: lowerLineY)/2.0);
	
	DataSource:: vertLineX = e->x();
	
	fprintf(stderr,"distance = %f\n",
		(DataSource::upperLineY-DataSource::lowerLineY)/DataSource::pixPerMicron);
		
	//usleep(200000);
	//repaint(false);
	// vw->newMidpoint = true;
    }
    
    if(cursor().shape() == (QCursor :: pointingHandCursor).shape())
    {
	// printf("Caught a hand\n");
	
	// calculate number of microns to move cursor onto crosshair
	
	float moveX = (DataSource::pixPerMicron*DataSource :: crossX + DataSource::zcenX  
		       - e -> x())/DataSource::pixPerMicron;
	float moveY = (DataSource::pixPerMicron*DataSource :: crossY + DataSource::zcenY
		       - e -> y())/DataSource::pixPerMicron;
	
	emit clickAndMoveMotors(-moveX, -moveY);
//	unsetCursor();
    }	
	
    //}
    
    /* Here we unfortunately hack together a refresh.
     * sorry, sorry, and sorry.
     * This is how it works - since the window "fixes itself" anytime it
     * it is covered by something and then uncovered, I decided to do just that -
     * xrefresh is a program that maps an invisible xwindow to the screen, and then
     * immediately unmaps it. I simply invoke it from here and tell it to draw a small
     * 1 pixel window in the center of the screen, and when it unmaps, voila we have a 
     * forced refresh....
     
     * Update - the following code has been commented out due to problems with threading
     QProcess *proc = new QProcess( this );
     proc->addArgument( "xrefresh" );
     proc->addArgument( "-geometry");
     proc->addArgument( "1x1+600+400");
     proc->start();
    */

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

void VideoWidget::setCrossHairEnabled( bool a )
{
    DataSource :: crossHairEnabled = a;
    
    if (a)  { unsetCursor(); }   // disable point-and-click centering
    if ((!DataSource::crossHairEnabled) && (!DataSource::midpointToolEnabled)) {
	 setCursor(QCursor(pointingHandCursor));  // reenable point-and-click centering	
    }
    
}


// turn on/off the midpoint tool
void VideoWidget::midpointEnabled( bool a )
{
    // if you enable the midpoint tool, show it too
    DataSource :: midpointToolEnabled = a;
    DataSource :: midpointTool = a;
    
    if (a)  { unsetCursor(); }   // disable point-and-click centering
    if ((!DataSource::crossHairEnabled) && (!DataSource::midpointToolEnabled)) {
	 setCursor(QCursor(pointingHandCursor));  // reenable point-and-click centering	
    }
    
}


void VideoWidget::crossHairDisplayed( bool a )
{
    DataSource :: crossHairDisplayed = a;
}


void VideoWidget::mouseReleaseEvent( QMouseEvent * e )
{
  fprintf(stderr,"%d %d \n",e->x(), e->y());
}


// turn on/off simple scale bar 
void VideoWidget::scaleBarDisplayed( bool a )
{
    DataSource :: barDisplayed = a;
}

void VideoWidget::paintEvent( QPaintEvent * )
{
    /*
        QPainter p;                       // our painter
        p.begin( this );                  // start painting the widget
        p.setPen( red );                  // red outline
        p.setBrush( yellow );             // yellow fill
        p.drawEllipse( 10, 20, 100,100 ); // 100x100 ellipse at position (10, 20)
        p.end();                          // painting done
*/	
}
