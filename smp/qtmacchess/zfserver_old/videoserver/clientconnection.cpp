#include <clientconnection.h>
#include <unistd.h>
#define LONG_PACK(a,b,c,d) ((long) (((long)(a))<<24) | (((long)(b))<<16) | (((long)(c))<<8)  |((long)(d)))
#define SWAP(a) ( (((a)&0x000000ff)<<24) | (((a)&0x0000ff00)<<8) | (((a)&0x00ff0000)>>8)  | (((a)&0xff000000)>>24) )


ClientConnection :: ClientConnection( int sock) : QSocket()
{
    connect( this, SIGNAL(readyRead()),
	     SLOT(readClient()) );
    connect( this, SIGNAL(connectionClosed()),
	     SLOT(terminateConnection()) );
    setSocket( sock );
    long test = LONG_PACK('M','P','4','U');
    test = SWAP(test);
    int i = this -> writeBlock((char *)(&test), (Q_ULONG)sizeof(long));
    printf("Wrote the header, status = %d\n", i);
}

ClientConnection ::  ~ClientConnection()
{
}

void ClientConnection :: readClient()
{
    // We don't need to read from the client, yet
    // Here is where we can put crosshair communication, etc
}

void ClientConnection :: terminateConnection()
{
    emit clientSocketClosed(this);
}
