void VideoWidget :: init()
{
    clientTable->setColumnWidth( 0, 100);
    clientTable->setColumnWidth( 1, 100);
    clientTable->setColumnWidth( 2, 150);
    socket = new QSocketDevice();
    mutex = new QMutex();
     vw = new VideoRenderer(this -> winId(), socket, mutex);
     vs = new VideoServer(socket, mutex);
     /*connect(vw -> vs, SIGNAL(clientAdded(QString, QString)),
	     this, SLOT( addClientToTable( QString,QString)));
     connect(vw -> vs, SIGNAL(clientRemoved(QString)),
	     this, SLOT( remClientFromTable( QString)));*/
     vw -> connect(this, SLOT(updateEnc(void)));
     vs -> connect(this, SLOT(toggleSocket(void)));
     
     // void connect( QObject *receiver, const char *timeMember, const char *sizeMember);
     vw -> start();
     vs -> start();
     serverStart = QDateTime ::  currentDateTime ();
}


void VideoWidget :: toggleSocket()
{
    mutex -> lock();
    if(!vw ->broadcast) 
    {
	printf("Turning on the socket\n");
	vw -> broadcast = true;
	vw -> keyframe = 1;
	
    }
    else 
    {
	printf("Turning off the socket\n");
	vw -> broadcast = false;
    }
    mutex -> unlock();
}


void VideoWidget::setCrossHair( int x, int y )
{
    vw -> crossX = x;
    vw -> crossY = y;
}


void VideoWidget::mouseDoubleClickEvent ( QMouseEvent * e )
{
    vw -> crossX = e -> x();
    vw -> crossY = e -> y();
    vw -> newCrossHair = true;
}


void VideoWidget::addClientToTable( QString hostname, QString ipAddress)
{
    QDateTime dt = QDateTime::currentDateTime();
    clientTable -> insertRows(0);
    clientTable ->setText( 0, 0, hostname);
    clientTable ->setText( 0, 1, ipAddress);
    clientTable ->setText( 0, 2, dt.toString("ddd MMM d, hh:mm ap"));
    int c = atoi(numClients -> text().ascii()) + 1;
    numClients -> setText(QString :: number(c));
}


void VideoWidget::remClientFromTable( QString ipAddress )
{
    for(int i = 0; i < clientTable -> numRows(); i++)
    {
	if(clientTable -> text( i, 1) == ipAddress)
	    clientTable -> removeRow(i);
    }
    int c = atoi(numClients -> text().ascii()) - 1;
    numClients -> setText(QString :: number(c));
    
}


void VideoWidget::updateEnc()
{
    int cf = atoi(currentFrame -> text().ascii()) + 1;
    currentFrame -> setText(QString :: number(cf));
    compressTime -> setText(QString :: number(vw -> time, 'f', 2));
    frameSize -> setText(QString :: number(vw -> size));
    updateUptime();
}

void VideoWidget :: updateUptime()
{
    QDateTime dt = QDateTime::currentDateTime();
    int i = serverStart.toTime_t();
    int elapsed = dt.toTime_t() - i;
    int days = elapsed / 86400;
    int hours = (elapsed - days*86400)/ 3600;
    int minutes = (elapsed - days*86400 - hours * 3600) / 60;
    int seconds = elapsed % 60;
    QString format;
    format.sprintf("%d day(s) %d hour(s) %d minute(s) %d second(s)", days, hours, minutes, seconds);
    uptime -> setText(format);
    
}


