#include <stdio.h>
#include "videoserver.h"
#include "clientconnection.h"
#include <qstring.h>


VideoServer :: VideoServer(QSocketDevice *socket, QMutex *mutex)
{
    this -> socket = socket;
    this -> mutex = mutex;
    signalSocket = new QSignal();
}


VideoServer :: ~VideoServer()
{
    
}

// This runs the server accept code in a separate thread
void VideoServer :: run()
{
    QHostAddress qHost;
    qHost.setAddress("000.000.000.000");    
    printf("Socket is valid?: %d\n", socket -> isValid());
    QSocketDevice *serverSocket = new QSocketDevice();
    serverSocket -> bind(qHost,1394);
    serverSocket -> listen (50);
    
    while(true)
    {
	char p;
	int fd = serverSocket -> accept();
	socket -> setSocket(fd,  QSocketDevice::Stream);
	printf("Socket Connected\n");
	printf("Socket is valid?: %d\n", socket -> isValid());
	
	long test = LONG_PACK('M','P','4','U');
	test = SWAP(test);
	int i = socket-> writeBlock((char *)(&test), (Q_ULONG)sizeof(long));
	printf("Wrote the header, status = %d\n", i);
	
	// this will turn on the broadcast
	signalSocket -> activate();
	
	// Once the socket reads something, it resets the connection
	socket -> readBlock(&p,1);
	
	// this will turn off the broadcast
	signalSocket -> activate();
    }
    
    
    /*
    emit clientAdded(socket -> peerName(),
		     socket -> peerAddress().toString());
		     */
}


void VideoServer :: connect( QObject *receiver, const char *member)
 {
     signalSocket ->connect( receiver, member );
 }



/*

void VideoServer :: newConnection( int socket )
{
    // lock mutex
    mutex.lock();


    ClientConnection *s = new ClientConnection(socket);
    connect(s, SIGNAL(clientSocketClosed(ClientConnection *)),
	    this, SLOT( removeClient(ClientConnection *)));
    sockets.append (s);
    keyframe = 1;

    // unlock mutex
    mutex.unlock();
    
    s-> ipAddress = s -> peerAddress().toString();
    QString peer = s -> peerName();
    if(peer == "") peer = "Not Available";
    emit clientAdded(peer, s -> ipAddress);
}


bool VideoServer :: isConnected()
    {

    if(sockets.count() == 0) return false;
	return true;
    }	

void VideoServer :: sendData(unsigned char *buf, long size)
{

    ClientConnection *temp;
    if(!isConnected()) return;

    for(temp = sockets.first();  sockets.at() != -1; temp = sockets.next())
    {
	int i;
	//printf("current socket = %d, number of connections = %d\n", sockets.at(), sockets.count());
	i = temp -> writeBlock((const char*)(&size), (Q_ULONG)(sizeof(long)));
	//printf("Wrote size to socket, i = %d,\n", i);
	i = temp -> writeBlock((const char *)buf, (Q_ULONG)size);
	//printf("Wrote block to socket, i = %d\n", i);
     }
}

int VideoServer :: newClient()
{
    if(keyframe == 1)
    {
	keyframe = -1;
	return 1;
    }
    return -1;
}

void VideoServer :: removeClient(ClientConnection *s)
{
    printf("Removed the terminated socket\n");
    sockets.remove(s);
    emit clientRemoved(s -> ipAddress);
    free(s);
}
*/
