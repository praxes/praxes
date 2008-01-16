#include <qserversocket.h>
#include <qptrlist.h>
#include <qmutex.h>
#include <qthread.h>
#include <qsignal.h>
#include <qsocketdevice.h>

#include "clientconnection.h"
#include "videorenderer.h"


#ifndef VIDEO_SERVER_H
#define VIDEO_SERVER_H

#define LONG_PACK(a,b,c,d) ((long) (((long)(a))<<24) | (((long)(b))<<16) | (((long)(c))<<8)  |((long)(d)))
#define SWAP(a) ( (((a)&0x000000ff)<<24) | (((a)&0x0000ff00)<<8) | (((a)&0x00ff0000)>>8)  | (((a)&0xff000000)>>24) )


class VideoServer : public QThread
{
public:
    VideoServer(VideoRenderer *vw, QSocketDevice *socket, QMutex *mutex);
    ~VideoServer();
    void run();
    void stop();
    void connect( QObject *receiver, const char *member);
    /*
    void newConnection( int socket );
    bool isConnected();
    void sendData(unsigned char *buf, long size);
    int newClient();
    */

    
private:
    QSocketDevice *socket;
    QSignal *signalSocket;
    QMutex *mutex;
    VideoRenderer *vw;
    //QPtrList<ClientConnection> sockets;
    /*
    ClientConnection *testclient;
    int keyframe;

signals:
  
    void clientAdded(QString, QString);
    void clientRemoved(QString);
    
public slots:
    void removeClient(ClientConnection *s); 
    */
};

#endif
