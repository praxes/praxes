#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <qlineedit.h>
#include <qmutex.h>
#include <qthread.h>
#include <qsignal.h>
#include "datasource.h"


class ZFThread : public QThread
{
    public:
    ZFThread();
    int connectZoomFocus(char *ipAddr);
    long send_command(char cmd, long inReg);
    void sigConnect( QObject *receiver, const char *member);
    void concurrentCommand(char sendCmd, long where);
    void run();
    void stop();
    private:
    QMutex mutex;
    int zfsocket_fd;
    struct sockaddr_in serv;
    QSignal *sig;
};
