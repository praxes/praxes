/****************************************************************************
** Form interface generated from reading ui file 'mainform.ui'
**
** Created: Sat Nov 6 11:56:55 2004
**      by: The User Interface Compiler ($Id: qt/main.cpp   3.1.2   edited Dec 19 11:45 $)
**
** WARNING! All changes made in this file will be lost!
****************************************************************************/

#ifndef MAINFORM_H
#define MAINFORM_H

#include <qvariant.h>
#include <qpixmap.h>
#include <qmainwindow.h>
#include <qsocket.h>
#include <qslider.h>
#include <kled.h>
#include "datasource.h"
#include "zfthread.h"

class QVBoxLayout;
class QHBoxLayout;
class QGridLayout;
class QAction;
class QActionGroup;
class QToolBar;
class QPopupMenu;
class VideoWidget;
class QPushButton;
class QButtonGroup;
class QLabel;
class QTextEdit;
class QFrame;
class QSlider;
class QSpinBox;
class QLineEdit;
class QSlider;

class MainForm : public QMainWindow
{
    Q_OBJECT

public:
    MainForm( QWidget* parent = 0, const char* name = 0, WFlags fl = WType_TopLevel );
    ~MainForm();

    QPushButton* pushButton15_4;
    QPushButton* pushButton15_5;
    QButtonGroup* telnetDiagnosticButtonGroup;
    QLabel* connectZoomFocusMotorLabel;
    QLabel* connectCompuMotorLabel;
    QPushButton* connectPushButton;
    QLabel* statusTextLabel;
    QLabel* connectVideoLabel;
    QTextEdit* telnetOutput;
    VideoWidget* videoWidget;
    QButtonGroup* pinButtonGroup;
    QPushButton* downPushButton;
    QPushButton* leftPushButton;
    QPushButton* inPushButton;
    QPushButton* outPushButton;
    QPushButton* upPushButton;
    QFrame* line1;
    QLabel* distanceMMLabel;
    QPushButton* rightPushButton;
    QButtonGroup* zoomFocusButtonGroup;
    QLabel* focusLabel;
    QLabel* zoomLabel;
    QSlider* zoomSlider;
    QSpinBox* focusSpinBox;
    QLabel* distanceLabel;
    QLineEdit* distanceLineEdit;
    QSlider* distanceSlider;
    QButtonGroup* rotationButtonGroup;
    QLineEdit* phiLineEdit;
    QLabel* labelPhiAngle;
    QPushButton* zeroPushButton;
    QPushButton* threeSixtyButton;
    QPushButton* oneEightyPushButton;
    QPushButton* negativeNinetyPushButton;
    QPushButton* ninetyPushButton;
    QPushButton* fivePushButton;
    QPushButton* fortyFivePushButton;
    QPushButton* negativeFivePushButton;
    QPushButton* negativeFortyFivePushButton;
    QMenuBar *MenuBar;
    QPopupMenu *FileMenu;
    QPopupMenu *VideoMenu;
    QPopupMenu *ToolsMenu;
    QAction* displayStream;
    QAction* motorsBeam_AlignmentAction;
    QAction* motorsnew_itemAction;
    QAction* stopStreamAction;
    QAction* videoQuitAction;
    QAction* fileSaveImageAction;
    QAction* fileQuitAction;
    QAction* midpointEnableAction;
    QAction* new_menuUnnamedAction;
    QAction* toolsmidpoint_toolAction;
    QAction* videoDisplay_Cross_HairAction;
    QAction* videoDisplay_Scale_BarAction;
    QAction* toolsClickMoveAction;
    QAction* toolsCrosshair_ToolAction;

public slots:
    virtual void updateCurrentZF();
    virtual void saveSnapshot();
    virtual void multiServerConnect();
    virtual void videoConnected();
    virtual void moveZoom( int value );
    virtual void moveFocus( int value );
    virtual void motorDisconnect();
    virtual void socketConnected();
    virtual void socketConnectionClosed();
    virtual void socketReadyRead();
    virtual void trev();
    virtual void clickAndMove();
    virtual void clickAndMoveMotors( float x, float y );
    virtual void upButton();
    virtual void downButton();
    virtual void rightButton();
    virtual void leftButton();
    virtual void rotateNinetyButton();
    virtual void rotateOneEightyButton();
    virtual void rotateNegativeNinetyButton();
    virtual void rotateNegativeFiveButton();
    virtual void rotateFiveButton();
    virtual void rotateFortyFiveButton();
    virtual void rotateNegativeFortyFiveButton();
    virtual void rotateZeroButton();
    virtual void updatePhiLineEdit();
    virtual void showSettingsDialog();
    virtual void distanceSliderChanged();
    virtual void zoomSliderChanged( int value );
    virtual void distanceLineEditChanged();
    virtual void fileSame_ImageAction_destroyed( QObject * );
    virtual void inButton();
    virtual void outButton();
    virtual void smallRotFw();
    virtual void smallRotBk();
    virtual void bigRotFw();
    virtual void bigRotBk();
    virtual void movePinOnClick( QMouseEvent * e );
    virtual void rotateThreeSixtyButton();
    virtual void syncAngle();

protected:
    float phiAngle;


protected slots:
    virtual void languageChange();

private:
    QSocket *socket;
    ZFThread *zfthread;

    QPixmap image0;

    void init();
    void destroy();

};

#endif // MAINFORM_H
