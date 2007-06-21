/****************************************************************************
** ui.h extension file, included from the uic-generated form implementation.
**
** If you wish to add, delete or rename functions or slots use
** Qt Designer which will update this file, preserving your code. Create an
** init() function in place of a constructor, and a destroy() function in
** place of a destructor.
*****************************************************************************/


void MainForm::init()
{
   //DataSource :: saveDefaults();
   DataSource :: initialize();
   zfthread = new ZFThread();
   zfthread -> sigConnect(this, SLOT(updateCurrentZF()));
   
   
}

void MainForm::destroy()
{
    DataSource :: save();
    motorDisconnect();
    videoWidget -> stop();
    //zfthread -> send_command(0x04, 0);
    //DataSource :: connectedToZoomFocus = false;

}

void MainForm :: updateCurrentZF()
{
//    currentZoomLineEdit-> setText(QString :: number(DataSource :: zoomCurrent));
 //   currentFocusLineEdit-> setText(QString :: number(DataSource :: focusCurrent));
}


void MainForm :: saveSnapshot()
{
    videoWidget -> saveImage();
}

void MainForm::multiServerConnect()
{
    /* first try and get the video working
     * it doesn't make sense to control the motors
     * if you can't see what you're doing
     */
    videoWidget -> start();
    
}


void MainForm :: videoConnected()
{    
    // connectPushButton -> setText("Connecting");
   // videoLED -> on();
    //fprintf(stderr, "We are now attempting to connect to CMOTOR 1\n");
    if(DataSource :: connectToMotor)
    {
	//fprintf(stderr, "We are now attempting to connect to CMOTOR 2\n");
	socket = new QSocket(this);
	connect( socket, SIGNAL(connected()),
		 SLOT(socketConnected()));
	connect( socket, SIGNAL(readyRead()),
		 SLOT(socketReadyRead()) );
	connect( socket, SIGNAL(connectionClosed()),
		 SLOT(socketConnectionClosed()) );
	socket->connectToHost(DataSource :: cmotorIP,  DataSource :: cmotorPort);
	
	// issue a QPHI command to determine the current angle
	
    }
    if(DataSource :: connectToZoomFocus)
    {

	long reg = 0;
	int i = zfthread -> connectZoomFocus((char *)DataSource :: zfmotorIP.ascii());
	if(i != 0)
	{
	    fprintf(stderr, "we had a problem connecting to zoom/focus\n");
	    zoomFocusButtonGroup -> setEnabled(false);
	}
	else
	{
		DataSource :: connectedToZoomFocus = true;
	//	zoomFocusMotorLED -> on();
		//fprintf(stderr, "value of motor 1: %d\n", send_command(0x01, (int)reg));
		zoomSlider -> setMaxValue(zfthread -> send_command(0x01, reg));
		//fprintf(stderr, "value of motor 2: %d\n", send_command(0x11, (int)reg));
           //  focusSlider -> setMaxValue(zfthread -> send_command(0x11, reg));    
		focusSpinBox -> setMaxValue(zfthread -> send_command(0x11, reg));    
		// focusSlider -> setMaxValue(4000);  
		zoomSlider -> setValue(zfthread -> send_command(0x02, reg));    
		// focusSlider -> setValue(zfthread -> send_command(0x12, reg));
		focusSpinBox -> setValue(zfthread -> send_command(0x12, reg));
		zfthread -> start();
		
		// set the slider to the previously stored value
      
		distanceSlider->setValue((int)10*log(1000*DataSource::pinStep));

		//fprintf(stderr, "current of motor 1:%d\n", send_command(0x02, (int)reg));
		//fprintf(stderr, "current of motor 2:%d\n", send_command(0x12, (int)reg));
	    }
	
	/*
	fprintf(stderr, "We are now attempting to connect to ZFMOTOR 1\n");
	zfsocket = new QSocket(this);
	connect( zfsocket, SIGNAL(connected()),
		 SLOT(zfsocketConnected()));
	//connect( zfsocket, SIGNAL(readyRead()),
	//	 SLOT(zfsocketReadyRead()) );
	connect( zfsocket, SIGNAL(connectionClosed()),
		 SLOT(socketConnectionClosed()) );
	zfsocket->connectToHost(DataSource :: zfmotorIP,  DataSource :: zfmotorPort);		*/
    }
}

void MainForm::moveZoom(int value)
{
    char distance[25];
    zfthread -> send_command(0x03, value);
    
  //   snprintf(distance, 25, "zoom %d", value);
     
     //currentZoomLineEdit -> setText(QString(distance));
    
//     telnetOutput->append(QString(distance));

    
    //snprintf(distance, 6, "%d", value);
    //currentZoomLineEdit -> setText(QString(distance));

}
	
void MainForm :: moveFocus(int value)
{
    //char distance[6];
    zfthread ->  send_command(0x13, value);
    //snprintf(distance, 6, "%d", value);
    //currentFocusLineEdit -> setText(QString(distance));
}
	
	
void MainForm::motorDisconnect()
{
    
    /*
    if(zfsocket -> state() == QSocket :: Connected) 
    {
	zfsocket -> putch(0x4);
	zfsocket->close();
    }
    */
    if(DataSource :: connectedToZoomFocus)
    {
	zfthread -> send_command(0x04, 0);
	// zoomFocusMotorLED -> off();
	DataSource :: connectedToZoomFocus = false;
    }
    if(DataSource :: connectedToMotor)
    {
    if(socket -> state() == QSocket :: Connected) socket->close();
    if ( socket->state() == QSocket::Closing ) 
    {
	// We have a delayed close.
	connect( socket, SIGNAL(delayedCloseFinished()),
		 SLOT(socketConnectionClosed()) );
    } 
    else 
    {
	// The socket is closed.
	socketConnectionClosed();
    }
}
    
    
    // videoWidget -> stop();
}

void MainForm::socketConnected()
{
    	//fprintf(stderr, "We are now attempting to connect to CMOTOR 3\n");
    // statusTextLabel -> setText("Status: Connected");
    pinButtonGroup -> setEnabled(true);
    rotationButtonGroup -> setEnabled(true);
    toolsClickMoveAction -> setEnabled(true);
    connectPushButton -> setText("Disconnect");
    QTextStream os(socket);
    os << "connect centering\n\0";
    DataSource :: connectedToMotor = true;
    DataSource :: motor_busy = false;
    disconnect( connectPushButton, 0, 0, 0 );
    connect( connectPushButton, SIGNAL(clicked()),
	     SLOT(motorDisconnect()));
    
    // compuMotorLED -> on();
  
    // read angle from data collection software
//	        os << "QPHI \nend_of_command\n";
}


/*
void MainForm::zfsocketConnected()
{
    connectPushButton -> setText("Disconnect");
    zoomFocusButtonGroup -> setEnabled(true);
    disconnect( connectPushButton, 0, 0, 0 );
    connect( connectPushButton, SIGNAL(clicked()),
	     SLOT(motorDisconnect()));
    DataSource :: connectedToZoomFocus = true;
    long reg;
    
    // Get ranges of zoom and focus motors    
    zfsocket -> putch(0x01); 
    zfsocket -> waitForMore (-1);
    zfsocket -> readBlock((char *)(&reg), sizeof(long));
    //zoomSlider -> setMaxValue(reg);
    
    fprintf(stderr, "reg1: %d\n", reg);
    zfsocket -> putch(0x11);
    zfsocket -> waitForMore (-1);
    zfsocket -> readBlock((char *)(&reg), sizeof(long));
    //focusSlider -> setMaxValue(reg);    
     fprintf(stderr, "reg1: %d\n", reg);
    // Get current position of zoom and focus motors
    zfsocket -> putch(0x02);
    zfsocket -> waitForMore (-1);
    zfsocket -> readBlock((char *)(&reg), sizeof(long));    
    //zoomSlider -> setValue(reg);
        fprintf(stderr, "reg1: %d\n", reg);
    zfsocket -> putch(0x12);    
    zfsocket -> waitForMore (-1);
    zfsocket -> readBlock((char *)(&reg), sizeof(long));        
    //focusSlider -> setValue(reg);
        fprintf(stderr, "reg1: %d\n", reg);
    connect( zfsocket, SIGNAL(readyRead()),
	 SLOT(zfsocketReadyRead()) );
}
*/



void MainForm::socketConnectionClosed()
{
    // statusTextLabel -> setText("Status: Disconnected");
    pinButtonGroup -> setEnabled(false);
    rotationButtonGroup -> setEnabled(false);
    toolsClickMoveAction -> setEnabled(false);
    disconnect( connectPushButton, 0, 0, 0 );
    connect( connectPushButton, SIGNAL(clicked()),
	     SLOT(videoConnected()));
    connectPushButton -> setText("Connect");
    // compuMotorLED -> off();
}


void MainForm::socketReadyRead()
{
    
    QString stmp;
    bool *ok=0;
    
    while(socket -> canReadLine()) 
           {
	stmp = socket -> readLine();
	
	if (stmp.contains("CMD_DONE")) {
	//  telnetOutput->append("CMD_DONE\n");
	    DataSource :: motor_busy = false;
	    pinButtonGroup -> setEnabled(true);
	    rotationButtonGroup -> setEnabled(true);
	    
	    // update the Phi angle is Marian's code changes it
	    
	} else if (stmp.contains("phi")) {
	
	    telnetOutput->append(stmp);   
	    phiAngle = stmp.remove("phi").toFloat(ok); 
	    // fprintf(stderr,"phiAngle = %f\n",phiAngle);    
                updatePhiLineEdit();
		     
	} else {telnetOutput->append(stmp);   
	    
	}
    } 
}

/*
void MainForm::zfsocketReadyRead()
{
  // Nothing yet
}
*/


void MainForm::trev()
{
    QTextStream os(socket);
    os << "trev\n";
}

void MainForm :: clickAndMove()
{
    videoWidget -> setCursor(QCursor(pointingHandCursor));
}


void MainForm :: clickAndMoveMotors(float x, float y)
{
    float ang = (phiAngle-45.0)*0.0174532925;
    
    QTextStream os(socket);
    
    /* moving on screen "x" direction == motor PinZ */
    //printf("Gonna output %f to pinz.\n", x / 1000.0);
    
    os << "MZ " << -x*DataSource::corZ / 1000.0 << "\nend_of_command\n";
    
    /* moving "y" == PinX, PinY */
    
    float pinx = y*DataSource::cor45*cos(ang);
    float piny = y*DataSource::cor135*sin(ang);
    
    //printf("Gonna output %f to pinx.\n", pinx / 1000.0);
    //printf("Gonna output %f to piny.\n", piny / 1000.0);
    
    os << "MX " << pinx / 1000.0 << "\nend_of_command\n";
    os << "MY " << piny / 1000.0 << "\nend_of_command\n";
}


// Move pins based on current phi angle. No need to mod angle.
// telnetOutput is for debugging, should probably shorten or remove
// when this stuff is all working.

void MainForm::upButton()
{
    QTextStream os(socket);
        
    char str[7];
    float x,y,delta,ang;
    
    delta = (distanceLineEdit->text()).toFloat();
    ang = (phiAngle-45.0)*0.0174532925;
    
    x = delta*DataSource::cor45*cos(ang);
    y = delta*DataSource::cor135*sin(ang);
    
    snprintf(str, 7, "%f",phiAngle);
    telnetOutput -> append("phi = " + QString(str) + "\n");
    
    // it is now possible to issue to commands thanks to mods Marian has
    // made to her code
    
	snprintf(str, 7, "%f",x); 
	telnetOutput -> append("PinX " + QString(str) + "\n");
 	os << "MX " + QString(str) + "\nend_of_command\n";
	
	snprintf(str, 7, "%f",y); 
	telnetOutput -> append("PinY " + QString(str) + "\n");
	os << "MY " + QString(str) + "\nend_of_command\n";
	
//	 pinButtonGroup -> setEnabled(false);
//	 rotationButtonGroup -> setEnabled(false);
 }

// same code as above only x,y are negative!

void MainForm::downButton()
{
    QTextStream os(socket);

    char str[7];
    float x,y,delta,ang;
    
    delta = (distanceLineEdit->text()).toFloat();
    ang = (phiAngle-45.0)*0.0174532925;
    
    x = -delta*DataSource::cor45*cos(ang);
    y = -delta*DataSource::cor135*sin(ang);
    
       snprintf(str, 7, "%f",phiAngle);
       telnetOutput -> append("phi = " + QString(str) + "\n");
     
      snprintf(str, 7, "%f",y); 
      telnetOutput -> append("Moving PinY " + QString(str) + "\n");
      os << "MY " + QString(str) + "\nend_of_command\n";
     
       snprintf(str, 7, "%f",x); 
       telnetOutput -> append("Moving PinX " + QString(str) + "\n");
       os << "MX " + QString(str) + "\nend_of_command\n";     

//      pinButtonGroup -> setEnabled(false);
//      rotationButtonGroup -> setEnabled(false);
      
  }

void MainForm::rightButton()
{
     char str[7];
     float delta;
    
     delta = DataSource::corZ*(distanceLineEdit->text()).toFloat();
     snprintf(str,7,"%f",-delta);
     
    QTextStream os(socket);
    telnetOutput -> append("PinZ " + QString(str) + "\n");
    os << "MZ " + QString(str) + "\nend_of_command\n";
    
 //   pinButtonGroup -> setEnabled(false);
 //   rotationButtonGroup -> setEnabled(false);
	 
}

void MainForm::leftButton()
{
    char str[7];
    float delta;
    delta =  DataSource::corZ*(distanceLineEdit -> text()).toFloat();
    snprintf(str,7,"%f",delta);
    
    QTextStream os(socket);
    os << "MZ " + QString(str) + "\nend_of_command\n";
    
 //    pinButtonGroup -> setEnabled(false);
 //    rotationButtonGroup -> setEnabled(false);
    
  telnetOutput -> append("PinZ " + distanceLineEdit -> text() + "\n");
}

void MainForm::rotateNinetyButton()
{
    QTextStream os(socket);
    os << "MPHI 90 \nend_of_command\n";
    rotationButtonGroup -> setEnabled(false);
    phiAngle += 90.0;
    // phiAngle = (int)phiAngle % 360;
     telnetOutput -> append("Phi +90\n");
     updatePhiLineEdit();
    
//     pinButtonGroup -> setEnabled(false);
//     rotationButtonGroup -> setEnabled(false);
	 
}

void MainForm::rotateOneEightyButton()
{
    QTextStream os(socket);
    
    // need to issue two commands due to Marian's code
    // see comments under rotateThreeSixtyButton
    
    os << "MPHI 90 \nend_of_command\n";
    os << "MPHI 90 \nend_of_command\n";
	
    phiAngle += 180.0;
    
  //  telnetOutput -> append("Phi +180\n");
 
    updatePhiLineEdit();
    
//    pinButtonGroup -> setEnabled(false);
  rotationButtonGroup -> setEnabled(false); 
    
}

void MainForm::rotateNegativeNinetyButton()
{
    QTextStream os(socket);
    os << "MPHI -90 \nend_of_command\n";
    phiAngle -= 90.0;
    rotationButtonGroup -> setEnabled(false); 
    
    //   telnetOutput -> append("Phi -90\n");

    updatePhiLineEdit();
}

void MainForm::rotateZeroButton()
{
    QTextStream os(socket);
    
 os << "HOMPHI end_of_command\n";
   
 //   os << "QPHI \n end_of_command\n";
    
   phiAngle = 45.0;
   
   telnetOutput -> append("setting phi to 45 deg ... please wait.\n");

   updatePhiLineEdit();
    
   // pinButtonGroup -> setEnabled(false);
     rotationButtonGroup -> setEnabled(false);
    
}

void MainForm::updatePhiLineEdit()
{
    char phi[7];
    
    // report angle as modulo
    
    snprintf(phi, 7, "%f", phiAngle - floorf(phiAngle/360.0)*360);
    phiLineEdit -> setText(QString(phi));
}

void MainForm::showSettingsDialog()
{
    SettingsDialog w;
    w.exec();
}


void MainForm::distanceSliderChanged()
{
    char distance[6];
    snprintf(distance, 6, "%f", exp((float) distanceSlider -> value()/10.0) / 1000.0);
    distanceLineEdit -> setText(QString(distance));
    
    // save stepsize
    
    DataSource::pinStep = exp((float) distanceSlider -> value()/10.0) / 1000.0;
    DataSource::save();

    
}


void MainForm::zoomSliderChanged(int value)
{
  //  char distance[7];
  //  snprintf(distance, 7, "%d", value);
  //  currentZoomLineEdit -> setText(QString(distance));
}



void MainForm::distanceLineEditChanged()
{
 //   distanceSlider -> setValue((int)((distanceLineEdit -> text()).toFloat() * 1000));
}


void MainForm::fileSame_ImageAction_destroyed( QObject * )
{

}

void MainForm::inButton()
{
  QTextStream os(socket);

    char str[7];
    float x,y,delta,ang;
    
    delta = (distanceLineEdit->text()).toFloat();
    ang = (phiAngle-45.0)*0.0174532925;
    
    y =   delta*DataSource::cor45*cos(ang);
    x =  -delta*DataSource::cor135*sin(ang);
    
    //  snprintf(str, 6, "%f",phiAngle);
    //  telnetOutput -> append("phi = " + QString(str) + "(deg)\n");
     
     snprintf(str, 7, "%f",y); 
     telnetOutput -> append("PinY " + QString(str) + "\n");
     os << "MY " + QString(str) + "\nend_of_command\n";
     
      snprintf(str, 7, "%f",x); 
      telnetOutput -> append("PinX " + QString(str) + "\n");
      os << "MX " + QString(str) + "\nend_of_command\n";     
          
}


void MainForm::outButton()
{
QTextStream os(socket);

    char str[7];
    float x,y,delta,ang;
    
    delta = (distanceLineEdit->text()).toFloat();
    ang = (phiAngle-45.0)*0.0174532925;
    
    y =  -delta*DataSource::cor45*cos(ang);
    x =   delta*DataSource::cor135*sin(ang);
    
       snprintf(str, 7, "%f",y); 
      telnetOutput -> append("PinY " + QString(str) + "\n");
      os << "MY " + QString(str) + "\nend_of_command\n";
     
      snprintf(str, 7, "%f",x); 
      telnetOutput -> append("PinX " + QString(str) + "\n");
      os << "MX " + QString(str) + "\nend_of_command\n";     
    
}


void MainForm::smallRotFw()
{
  QTextStream os(socket);
 
     os << "MPHI 5.0\nend_of_command\n";
     
    phiAngle += 5;
     
    updatePhiLineEdit();
    
 //   pinButtonGroup -> setEnabled(false);
 //   rotationButtonGroup -> setEnabled(false);    
    
}


void MainForm::smallRotBk()
{
 QTextStream os(socket);
 
     os << "MPHI -5.0\nend_of_command\n";
     
    phiAngle -= 5;
     
    updatePhiLineEdit();
    
 //   pinButtonGroup -> setEnabled(false);
 //   rotationButtonGroup -> setEnabled(false);    
    
}


void MainForm::bigRotFw()
{
    QTextStream os(socket);
 
    // char str[6];
     
     os << "MPHI 45.0\nend_of_command\n";
     
    phiAngle += 45;
     
    updatePhiLineEdit();
    
 //   pinButtonGroup -> setEnabled(false);
 //   rotationButtonGroup -> setEnabled(false);    
    
}


void MainForm::bigRotBk()
{
 QTextStream os(socket);
     
  //   os << "MPHI -45.0\nend_of_command\n";
 
 os << "QPHI \n end_of_command \n";
 
//     phiAngle -= 45;
     
//    updatePhiLineEdit();
    
 //   pinButtonGroup -> setEnabled(false);
 //   rotationButtonGroup -> setEnabled(false);    
    
}


// This routine is called when VideoWidget is clicked once

void MainForm::movePinOnClick(QMouseEvent *e)
{

    QString sx;
    QString sy;
    
     sx.number(e->x());   sy.number(e->y());
    
      telnetOutput -> append("(" + sx + "," + sy + ")");
}


void MainForm::rotateThreeSixtyButton()
{
QTextStream os(socket);
     
// have to use multiple +90 commands here because
// Marian's code computes the shortest direction of motion
// to get the final angle (not always the same direction)

     os << "MPHI 90.0\nend_of_command\n";
          phiAngle += 90.0;
     updatePhiLineEdit();
     rotationButtonGroup -> setEnabled(false);
     os << "MPHI 90.0\nend_of_command\n";
          phiAngle += 90.0;
     updatePhiLineEdit();
     rotationButtonGroup -> setEnabled(false);
     os << "MPHI 90.0\nend_of_command\n";
          phiAngle += 90.0;
     updatePhiLineEdit();
     rotationButtonGroup -> setEnabled(false);
     os << "MPHI 90.0\nend_of_command\n";
          phiAngle += 90.0;
     updatePhiLineEdit();
     rotationButtonGroup -> setEnabled(false);
     
}


void MainForm::syncAngle()
{
    QTextStream os(socket);
 
      os << "QPHI \nend_of_command\n";
    
    }




