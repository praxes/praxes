/****************************************************************************
** Form interface generated from reading ui file 'video/videowidget.ui'
**
** Created: Thu Jan 22 16:48:06 2004
**      by: The User Interface Compiler ($Id: videowidget.h,v 1.1.1.1 2004/05/26 18:51:10 degani Exp $)
**
** WARNING! All changes made in this file will be lost!
****************************************************************************/

#ifndef VIDEOWIDGET_H
#define VIDEOWIDGET_H

#include <qvariant.h>
#include <qfile.h>
#include <qwidget.h>
#include "videorenderer.h"

class QVBoxLayout;
class QHBoxLayout;
class QGridLayout;

class VideoWidget : public QWidget
{
    Q_OBJECT

public:
    VideoWidget( QWidget* parent = 0, const char* name = 0, WFlags fl = 0 );
    ~VideoWidget();


public slots:
    virtual void start( QString videoIP, int port );
    virtual void stop();
    virtual void setCrossHair( int x, int y );
    virtual void mouseDoubleClickEvent( QMouseEvent * e );
    virtual void setCrossHairEnabled( bool a );
    virtual void midpointEnabled( bool a );
    virtual void crossHairDisplayed( bool a );
    virtual void mouseReleaseEvent( QMouseEvent * e );
    virtual void scaleBarDisplayed( bool a );

protected:
    bool midpointToolEnabled;
    bool crossHairEnabled;
    int newVariable;


protected slots:
    virtual void languageChange();
private:
    int upperLineY;
    int lowerLineY;
    int centerY;
    int centerX;
    int midLineY;
    VideoRenderer *vw;

    void init();
    void destroy();

};

#endif // VIDEOWIDGET_H
