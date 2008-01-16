/****************************************************************************
** Form interface generated from reading ui file 'videowidget.ui'
**
** Created: Fri Oct 1 17:09:35 2004
**      by: The User Interface Compiler ($Id: qt/main.cpp   3.1.1   edited Nov 21 17:40 $)
**
** WARNING! All changes made in this file will be lost!
****************************************************************************/

#ifndef VIDEOWIDGET_H
#define VIDEOWIDGET_H

#include <qvariant.h>
#include <qdatetime.h>
#include <qsocketdevice.h>
#include <qtable.h>
#include <qwidget.h>
#include "videorenderer.h"
#include "videoserver.h"

class QVBoxLayout;
class QHBoxLayout;
class QGridLayout;
class QButtonGroup;
class QFrame;
class QLabel;
class QLineEdit;
class QTable;

class VideoWidget : public QWidget
{
    Q_OBJECT

public:
    VideoWidget( QWidget* parent = 0, const char* name = 0, WFlags fl = 0 );
    ~VideoWidget();

    QFrame* controlFrame;
    QButtonGroup* clientGroup;
    QLineEdit* numClients;
    QLabel* clientLabel;
    QTable* clientTable;
    QButtonGroup* xvidGroup;
    QLabel* xvidLabel;
    QLabel* currentFrameLabel;
    QLabel* compressTimeLabel;
    QLabel* frameSizeLabel;
    QLineEdit* currentFrame;
    QLineEdit* compressTime;
    QLineEdit* frameSize;
    QButtonGroup* uptimeGroup;
    QLabel* uptimeLabel;
    QLabel* serverLabel;
    QLineEdit* uptime;

public slots:
    virtual void toggleSocket();
    virtual void setCrossHair( int x, int y );
    virtual void mouseDoubleClickEvent( QMouseEvent * e );
    virtual void addClientToTable( QString hostname, QString ipAddress );
    virtual void remClientFromTable( QString ipAddress );
    virtual void updateEnc();
    virtual void updateUptime();

protected:
    VideoRenderer *vw;
    QSocketDevice *socket;
    VideoServer *vs;
    QMutex *mutex;


protected slots:
    virtual void languageChange();
private:
    QDateTime serverStart;

    void init();

};

#endif // VIDEOWIDGET_H
