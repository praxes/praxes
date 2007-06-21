/****************************************************************************
** Form interface generated from reading ui file 'videowidget.ui'
**
** Created: Sat Nov 6 11:37:40 2004
**      by: The User Interface Compiler ($Id: qt/main.cpp   3.1.2   edited Dec 19 11:45 $)
**
** WARNING! All changes made in this file will be lost!
****************************************************************************/

#ifndef VIDEOWIDGET_H
#define VIDEOWIDGET_H

#include <qvariant.h>
#include <qwidget.h>
#include <qfile.h>
#include <qpaintdevice.h>
#include <qpainter.h>
#include <qprocess.h>
#include "videorenderer.h"
#include "../datasource.h"

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
    virtual void saveImage();
    virtual void start();
    virtual void stop();
    virtual void setCrossHair( int x, int y );
    virtual void mouseDoubleClickEvent( QMouseEvent * e );
    virtual void setCrossHairEnabled( bool a );
    virtual void midpointEnabled( bool a );
    virtual void crossHairDisplayed( bool a );
    virtual void mouseReleaseEvent( QMouseEvent * e );
    virtual void scaleBarDisplayed( bool a );

signals:
    void videoConnected();
    void clickAndMoveMotors(float, float);

protected:
    virtual void paintEvent( QPaintEvent * );


protected slots:
    virtual void languageChange();

private:
    VideoRenderer *vw;

    void init();
    void destroy();

};

#endif // VIDEOWIDGET_H
