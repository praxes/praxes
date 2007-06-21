#include "zfthread.h"
#include "qprocess.h"

ZFThread :: ZFThread()
{
    sig = new QSignal();
}

int ZFThread :: connectZoomFocus(char *ipAddr)
{
  int i;
  zfsocket_fd = socket(AF_INET,SOCK_STREAM,0);
  // printf("socket returned: %d\n",zfsocket_fd);
  serv.sin_family=AF_INET;
  inet_aton(ipAddr,&(serv.sin_addr));
  // printf("127.0.0.1 is really: %d\n",serv.sin_addr);
  serv.sin_port=htons(4001);
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
	return reg;
    case 0x3:
	mutex.lock();
	//fprintf(stderr, "Move Request Locked Mutex\n");
	write(zfsocket_fd, &cmd, 1);
	write(zfsocket_fd,&inReg,4);
	//fprintf(stderr, "Moved the motor to %d\n", inReg);
	mutex.unlock();
	//fprintf(stderr, "Move Request UnLocked Mutex\n");
	return 0;
    case 0x4:
	mutex.lock();
	write(zfsocket_fd, &cmd, 1); 
	close(zfsocket_fd);
	zfsocket_fd = -1;
	DataSource :: connectedToZoomFocus = false;
	mutex.unlock();
	return 0;
    default:
	return 0;
    }
    return 0;
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
	
	DataSource :: pixPerMicron = exp(9.10281e-5*reg-1.28814);
	
	// HACK - to refresh crosshairs
	if(reg + 50 < DataSource :: zoomCurrent || reg -50 > DataSource :: zoomCurrent)
	{
	    QProcess *proc = new QProcess();
	    proc->addArgument( "xrefresh" );
	    proc->addArgument( "-geometry");
	    proc->addArgument( "1x1+600+400");
	    proc->start();
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

