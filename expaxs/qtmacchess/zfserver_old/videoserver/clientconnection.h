#include <qsocket.h>
#include <stdio.h>

#ifndef CLIENT_CONNECTION_H
#define CLIENT_CONNECTION_H


class ClientConnection: public QSocket
{
       Q_OBJECT
public:
    ClientConnection( int sock);
    ~ClientConnection();
     QString ipAddress;
signals:
    void clientSocketClosed(ClientConnection *s);

public slots:
   void readClient();
   void terminateConnection();
};

#endif
