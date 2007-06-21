/****************************************************************************
** Form implementation generated from reading ui file 'mainform.ui'
**
** Created: Sat Nov 6 11:57:14 2004
**      by: The User Interface Compiler ($Id: qt/main.cpp   3.1.2   edited Dec 19 11:45 $)
**
** WARNING! All changes made in this file will be lost!
****************************************************************************/

#include "mainform.h"

#include <qvariant.h>
#include <qfile.h>
#include <./video/.ui/videowidget.h>
#include <qpushbutton.h>
#include <qbuttongroup.h>
#include <qlabel.h>
#include <qtextedit.h>
#include <qframe.h>
#include <qslider.h>
#include <qspinbox.h>
#include <qlineedit.h>
#include <qlayout.h>
#include <qtooltip.h>
#include <qwhatsthis.h>
#include <qaction.h>
#include <qmenubar.h>
#include <qpopupmenu.h>
#include <qtoolbar.h>
#include <qimage.h>
#include <qpixmap.h>

#include "settingsdialog.h"
#include "../mainform.ui.h"
/* 
 *  Constructs a MainForm as a child of 'parent', with the 
 *  name 'name' and widget flags set to 'f'.
 *
 */
MainForm::MainForm( QWidget* parent, const char* name, WFlags fl )
    : QMainWindow( parent, name, fl )
{
    (void)statusBar();
    if ( !name )
	setName( "MainForm" );
    setMinimumSize( QSize( 21, 93 ) );
    setCentralWidget( new QWidget( this, "qt_central_widget" ) );

    pushButton15_4 = new QPushButton( centralWidget(), "pushButton15_4" );
    pushButton15_4->setGeometry( QRect( 20, 26, 20, 20 ) );

    pushButton15_5 = new QPushButton( centralWidget(), "pushButton15_5" );
    pushButton15_5->setGeometry( QRect( 20, 26, 20, 20 ) );

    telnetDiagnosticButtonGroup = new QButtonGroup( centralWidget(), "telnetDiagnosticButtonGroup" );
    telnetDiagnosticButtonGroup->setGeometry( QRect( 490, 780, 530, 160 ) );
    telnetDiagnosticButtonGroup->setPaletteBackgroundColor( QColor( 230, 230, 230 ) );

    connectZoomFocusMotorLabel = new QLabel( telnetDiagnosticButtonGroup, "connectZoomFocusMotorLabel" );
    connectZoomFocusMotorLabel->setGeometry( QRect( 400, 90, 121, 20 ) );

    connectCompuMotorLabel = new QLabel( telnetDiagnosticButtonGroup, "connectCompuMotorLabel" );
    connectCompuMotorLabel->setGeometry( QRect( 400, 70, 110, 20 ) );

    connectPushButton = new QPushButton( telnetDiagnosticButtonGroup, "connectPushButton" );
    connectPushButton->setGeometry( QRect( 380, 125, 140, 25 ) );

    statusTextLabel = new QLabel( telnetDiagnosticButtonGroup, "statusTextLabel" );
    statusTextLabel->setGeometry( QRect( 380, 20, 140, 24 ) );
    statusTextLabel->setFrameShape( QLabel::Box );
    statusTextLabel->setFrameShadow( QLabel::Sunken );
    statusTextLabel->setAlignment( int( QLabel::AlignCenter ) );

    connectVideoLabel = new QLabel( telnetDiagnosticButtonGroup, "connectVideoLabel" );
    connectVideoLabel->setGeometry( QRect( 400, 50, 110, 20 ) );

    telnetOutput = new QTextEdit( telnetDiagnosticButtonGroup, "telnetOutput" );
    telnetOutput->setGeometry( QRect( 10, 20, 360, 130 ) );
    telnetOutput->setReadOnly( TRUE );

    videoWidget = new VideoWidget( centralWidget(), "videoWidget" );
    videoWidget->setEnabled( TRUE );
    videoWidget->setGeometry( QRect( 0, 0, 1024, 768 ) );
    videoWidget->setSizePolicy( QSizePolicy( (QSizePolicy::SizeType)5, (QSizePolicy::SizeType)5, 0, 0, videoWidget->sizePolicy().hasHeightForWidth() ) );
    videoWidget->setPaletteBackgroundColor( QColor( 0, 0, 0 ) );

    pinButtonGroup = new QButtonGroup( centralWidget(), "pinButtonGroup" );
    pinButtonGroup->setEnabled( FALSE );
    pinButtonGroup->setGeometry( QRect( 10, 780, 290, 160 ) );

    downPushButton = new QPushButton( pinButtonGroup, "downPushButton" );
    downPushButton->setGeometry( QRect( 50, 105, 40, 40 ) );
    downPushButton->setPixmap( QPixmap::fromMimeSource( "3.xpm" ) );

    leftPushButton = new QPushButton( pinButtonGroup, "leftPushButton" );
    leftPushButton->setGeometry( QRect( 10, 65, 40, 40 ) );
    leftPushButton->setPixmap( QPixmap::fromMimeSource( "4.xpm" ) );

    inPushButton = new QPushButton( pinButtonGroup, "inPushButton" );
    inPushButton->setGeometry( QRect( 50, 65, 40, 20 ) );

    outPushButton = new QPushButton( pinButtonGroup, "outPushButton" );
    outPushButton->setGeometry( QRect( 50, 85, 40, 20 ) );

    upPushButton = new QPushButton( pinButtonGroup, "upPushButton" );
    upPushButton->setGeometry( QRect( 50, 25, 40, 40 ) );
    upPushButton->setPixmap( QPixmap::fromMimeSource( "1.xpm" ) );

    line1 = new QFrame( pinButtonGroup, "line1" );
    line1->setGeometry( QRect( 130, 20, 20, 130 ) );
    line1->setFrameShape( QFrame::VLine );
    line1->setFrameShadow( QFrame::Sunken );
    line1->setFrameShape( QFrame::VLine );

    distanceMMLabel = new QLabel( pinButtonGroup, "distanceMMLabel" );
    distanceMMLabel->setGeometry( QRect( 250, 45, 30, 21 ) );
    distanceMMLabel->setAlignment( int( QLabel::AlignCenter ) );

    rightPushButton = new QPushButton( pinButtonGroup, "rightPushButton" );
    rightPushButton->setGeometry( QRect( 90, 65, 40, 40 ) );
    rightPushButton->setPixmap( QPixmap::fromMimeSource( "2.xpm" ) );

    zoomFocusButtonGroup = new QButtonGroup( pinButtonGroup, "zoomFocusButtonGroup" );
    zoomFocusButtonGroup->setGeometry( QRect( 140, 70, 141, 80 ) );
    zoomFocusButtonGroup->setLineWidth( 0 );

    focusLabel = new QLabel( zoomFocusButtonGroup, "focusLabel" );
    focusLabel->setGeometry( QRect( 10, 50, 50, 21 ) );

    zoomLabel = new QLabel( zoomFocusButtonGroup, "zoomLabel" );
    zoomLabel->setGeometry( QRect( 10, 20, 130, 21 ) );

    zoomSlider = new QSlider( zoomFocusButtonGroup, "zoomSlider" );
    zoomSlider->setGeometry( QRect( 10, 0, 131, 20 ) );
    zoomSlider->setOrientation( QSlider::Horizontal );
    zoomSlider->setTickmarks( QSlider::NoMarks );
    zoomSlider->setTickInterval( 100 );

    focusSpinBox = new QSpinBox( zoomFocusButtonGroup, "focusSpinBox" );
    focusSpinBox->setGeometry( QRect( 60, 50, 80, 22 ) );
    focusSpinBox->setAcceptDrops( TRUE );
    focusSpinBox->setLineStep( 50 );

    distanceLabel = new QLabel( pinButtonGroup, "distanceLabel" );
    distanceLabel->setGeometry( QRect( 150, 45, 60, 20 ) );

    distanceLineEdit = new QLineEdit( pinButtonGroup, "distanceLineEdit" );
    distanceLineEdit->setGeometry( QRect( 210, 45, 40, 20 ) );

    distanceSlider = new QSlider( pinButtonGroup, "distanceSlider" );
    distanceSlider->setGeometry( QRect( 150, 25, 130, 20 ) );
    distanceSlider->setMinValue( 0 );
    distanceSlider->setMaxValue( 63 );
    distanceSlider->setLineStep( 150 );
    distanceSlider->setPageStep( 150 );
    distanceSlider->setValue( 63 );
    distanceSlider->setOrientation( QSlider::Horizontal );
    distanceSlider->setTickmarks( QSlider::NoMarks );
    distanceSlider->setTickInterval( 500 );

    rotationButtonGroup = new QButtonGroup( centralWidget(), "rotationButtonGroup" );
    rotationButtonGroup->setEnabled( FALSE );
    rotationButtonGroup->setGeometry( QRect( 310, 780, 170, 160 ) );

    phiLineEdit = new QLineEdit( rotationButtonGroup, "phiLineEdit" );
    phiLineEdit->setEnabled( FALSE );
    phiLineEdit->setGeometry( QRect( 90, 20, 60, 21 ) );
    phiLineEdit->setReadOnly( TRUE );

    labelPhiAngle = new QLabel( rotationButtonGroup, "labelPhiAngle" );
    labelPhiAngle->setGeometry( QRect( 20, 20, 70, 20 ) );

    zeroPushButton = new QPushButton( rotationButtonGroup, "zeroPushButton" );
    zeroPushButton->setGeometry( QRect( 20, 50, 130, 30 ) );

    threeSixtyButton = new QPushButton( rotationButtonGroup, "threeSixtyButton" );
    threeSixtyButton->setGeometry( QRect( 130, 130, 31, 21 ) );

    oneEightyPushButton = new QPushButton( rotationButtonGroup, "oneEightyPushButton" );
    oneEightyPushButton->setGeometry( QRect( 90, 130, 31, 21 ) );

    negativeNinetyPushButton = new QPushButton( rotationButtonGroup, "negativeNinetyPushButton" );
    negativeNinetyPushButton->setGeometry( QRect( 50, 130, 31, 21 ) );

    ninetyPushButton = new QPushButton( rotationButtonGroup, "ninetyPushButton" );
    ninetyPushButton->setGeometry( QRect( 10, 130, 31, 21 ) );

    fivePushButton = new QPushButton( rotationButtonGroup, "fivePushButton" );
    fivePushButton->setGeometry( QRect( 90, 100, 31, 21 ) );

    fortyFivePushButton = new QPushButton( rotationButtonGroup, "fortyFivePushButton" );
    fortyFivePushButton->setGeometry( QRect( 130, 100, 31, 21 ) );

    negativeFivePushButton = new QPushButton( rotationButtonGroup, "negativeFivePushButton" );
    negativeFivePushButton->setGeometry( QRect( 50, 100, 31, 21 ) );

    negativeFortyFivePushButton = new QPushButton( rotationButtonGroup, "negativeFortyFivePushButton" );
    negativeFortyFivePushButton->setGeometry( QRect( 10, 100, 31, 21 ) );

    // actions
    displayStream = new QAction( this, "displayStream" );
    displayStream->setIconSet( QIconSet( QPixmap::fromMimeSource( "video.jpg" ) ) );
    motorsBeam_AlignmentAction = new QAction( this, "motorsBeam_AlignmentAction" );
    motorsBeam_AlignmentAction->setToggleAction( TRUE );
    motorsnew_itemAction = new QAction( this, "motorsnew_itemAction" );
    stopStreamAction = new QAction( this, "stopStreamAction" );
    stopStreamAction->setIconSet( QIconSet( QPixmap::fromMimeSource( "stop.jpeg" ) ) );
    videoQuitAction = new QAction( this, "videoQuitAction" );
    fileSaveImageAction = new QAction( this, "fileSaveImageAction" );
    fileSaveImageAction->setIconSet( QIconSet( QPixmap::fromMimeSource( "filesave" ) ) );
    fileQuitAction = new QAction( this, "fileQuitAction" );
    midpointEnableAction = new QAction( this, "midpointEnableAction" );
    new_menuUnnamedAction = new QAction( this, "new_menuUnnamedAction" );
    toolsmidpoint_toolAction = new QAction( this, "toolsmidpoint_toolAction" );
    toolsmidpoint_toolAction->setToggleAction( TRUE );
    videoDisplay_Cross_HairAction = new QAction( this, "videoDisplay_Cross_HairAction" );
    videoDisplay_Cross_HairAction->setToggleAction( TRUE );
    videoDisplay_Cross_HairAction->setOn( TRUE );
    videoDisplay_Scale_BarAction = new QAction( this, "videoDisplay_Scale_BarAction" );
    videoDisplay_Scale_BarAction->setToggleAction( TRUE );
    videoDisplay_Scale_BarAction->setOn( TRUE );
    toolsClickMoveAction = new QAction( this, "toolsClickMoveAction" );
    toolsClickMoveAction->setToggleAction( FALSE );
    toolsClickMoveAction->setEnabled( FALSE );
    toolsCrosshair_ToolAction = new QAction( this, "toolsCrosshair_ToolAction" );
    toolsCrosshair_ToolAction->setToggleAction( TRUE );


    // toolbars


    // menubar
    MenuBar = new QMenuBar( this, "MenuBar" );

    MenuBar->setGeometry( QRect( 0, 0, 1024, 30 ) );
    FileMenu = new QPopupMenu( this );

    fileSaveImageAction->addTo( FileMenu );
    FileMenu->insertSeparator();
    fileQuitAction->addTo( FileMenu );
    MenuBar->insertItem( QString(""), FileMenu, 0 );
    VideoMenu = new QPopupMenu( this );

    videoDisplay_Scale_BarAction->addTo( VideoMenu );
    videoDisplay_Cross_HairAction->addTo( VideoMenu );
    MenuBar->insertItem( QString(""), VideoMenu, 1 );
    ToolsMenu = new QPopupMenu( this );

    toolsmidpoint_toolAction->addTo( ToolsMenu );
    toolsCrosshair_ToolAction->addTo( ToolsMenu );
    toolsClickMoveAction->addTo( ToolsMenu );
    MenuBar->insertItem( QString(""), ToolsMenu, 2 );

    languageChange();
    resize( QSize(1024, 1028).expandedTo(minimumSizeHint()) );
    clearWState( WState_Polished );

    // signals and slots connections
    connect( outPushButton, SIGNAL( clicked() ), this, SLOT( outButton() ) );
    connect( inPushButton, SIGNAL( clicked() ), this, SLOT( inButton() ) );
    connect( distanceSlider, SIGNAL( valueChanged(int) ), this, SLOT( distanceSliderChanged() ) );
    connect( distanceLineEdit, SIGNAL( textChanged(const QString&) ), this, SLOT( distanceLineEditChanged() ) );
    connect( oneEightyPushButton, SIGNAL( clicked() ), this, SLOT( rotateOneEightyButton() ) );
    connect( negativeNinetyPushButton, SIGNAL( clicked() ), this, SLOT( rotateNegativeNinetyButton() ) );
    connect( ninetyPushButton, SIGNAL( clicked() ), this, SLOT( rotateNinetyButton() ) );
    connect( zeroPushButton, SIGNAL( clicked() ), this, SLOT( rotateZeroButton() ) );
    connect( downPushButton, SIGNAL( clicked() ), this, SLOT( downButton() ) );
    connect( rightPushButton, SIGNAL( clicked() ), this, SLOT( rightButton() ) );
    connect( leftPushButton, SIGNAL( clicked() ), this, SLOT( leftButton() ) );
    connect( upPushButton, SIGNAL( clicked() ), this, SLOT( upButton() ) );
    connect( connectPushButton, SIGNAL( clicked() ), this, SLOT( multiServerConnect() ) );
    connect( zoomSlider, SIGNAL( sliderMoved(int) ), this, SLOT( moveZoom(int) ) );
    connect( fileSaveImageAction, SIGNAL( activated() ), this, SLOT( saveSnapshot() ) );
    connect( toolsClickMoveAction, SIGNAL( activated() ), this, SLOT( clickAndMove() ) );
    connect( focusSpinBox, SIGNAL( valueChanged(int) ), this, SLOT( moveFocus(int) ) );
    connect( threeSixtyButton, SIGNAL( clicked() ), this, SLOT( rotateThreeSixtyButton() ) );
    connect( videoDisplay_Scale_BarAction, SIGNAL( toggled(bool) ), videoWidget, SLOT( scaleBarDisplayed(bool) ) );
    connect( videoDisplay_Cross_HairAction, SIGNAL( toggled(bool) ), videoWidget, SLOT( crossHairDisplayed(bool) ) );
    connect( toolsmidpoint_toolAction, SIGNAL( toggled(bool) ), videoWidget, SLOT( midpointEnabled(bool) ) );
    connect( videoWidget, SIGNAL( videoConnected() ), this, SLOT( videoConnected() ) );
    connect( videoWidget, SIGNAL( clickAndMoveMotors(float,float) ), this, SLOT( clickAndMoveMotors(float,float) ) );
    connect( toolsCrosshair_ToolAction, SIGNAL( toggled(bool) ), videoWidget, SLOT( setCrossHairEnabled(bool) ) );
    connect( fivePushButton, SIGNAL( clicked() ), this, SLOT( rotateFiveButton() ) );
    connect( fortyFivePushButton, SIGNAL( clicked() ), this, SLOT( rotateFortyFiveButton() ) );
    connect( negativeFortyFivePushButton, SIGNAL( clicked() ), this, SLOT( rotateNegativeFortyFiveButton() ) );
    connect( negativeFivePushButton, SIGNAL( clicked() ), this, SLOT( rotateNegativeFiveButton() ) );
    init();
}

/*
 *  Destroys the object and frees any allocated resources
 */
MainForm::~MainForm()
{
    destroy();
    // no need to delete child widgets, Qt does it all for us
}

/*
 *  Sets the strings of the subwidgets using the current
 *  language.
 */
void MainForm::languageChange()
{
    setCaption( tr( "Macchess 1394 Streaming / Centering Project" ) );
    pushButton15_4->setText( tr( "pushButton15" ) );
    pushButton15_5->setText( tr( "pushButton15" ) );
    telnetDiagnosticButtonGroup->setTitle( tr( "Motor Control / Video Stream Diagnostics" ) );
    connectZoomFocusMotorLabel->setText( tr( "Zoom/Focus Motors" ) );
    connectCompuMotorLabel->setText( tr( "XYZ Phi Motors" ) );
    connectPushButton->setText( tr( "Connect" ) );
    statusTextLabel->setText( tr( "Connection Status" ) );
    connectVideoLabel->setText( tr( "MPEG-4 Video" ) );
    pinButtonGroup->setTitle( tr( "XYZ Axis / Zoom Focus Motors" ) );
    downPushButton->setText( QString::null );
    leftPushButton->setText( QString::null );
    inPushButton->setText( tr( "in" ) );
    outPushButton->setText( tr( "out" ) );
    upPushButton->setText( QString::null );
    distanceMMLabel->setText( tr( "mm" ) );
    rightPushButton->setText( QString::null );
    zoomFocusButtonGroup->setTitle( QString::null );
    focusLabel->setText( tr( "focus:" ) );
    zoomLabel->setText( tr( "out       - zoom -      in" ) );
    distanceLabel->setText( tr( "step size:" ) );
    distanceLineEdit->setText( tr( "0.544" ) );
    rotationButtonGroup->setTitle( tr( "Rotational Controls" ) );
    phiLineEdit->setText( tr( "0.0" ) );
    labelPhiAngle->setText( tr( "Phi Angle:" ) );
    zeroPushButton->setText( tr( "home" ) );
    threeSixtyButton->setText( tr( "+360" ) );
    oneEightyPushButton->setText( tr( "+180" ) );
    negativeNinetyPushButton->setText( tr( "-90" ) );
    ninetyPushButton->setText( tr( "+90" ) );
    fivePushButton->setText( tr( "+5" ) );
    fortyFivePushButton->setText( tr( "+45" ) );
    negativeFivePushButton->setText( tr( "-5" ) );
    negativeFortyFivePushButton->setText( tr( "-45" ) );
    displayStream->setText( tr( "Start MPEG-4 Video Stream" ) );
    motorsBeam_AlignmentAction->setText( tr( "Beam Alignment" ) );
    motorsnew_itemAction->setText( tr( "new item" ) );
    stopStreamAction->setText( tr( "Stop Video Stream" ) );
    videoQuitAction->setText( tr( "&Quit" ) );
    fileSaveImageAction->setText( tr( "Save Snapshot" ) );
    fileSaveImageAction->setMenuText( tr( "Save Image" ) );
    fileSaveImageAction->setToolTip( tr( "Save Image" ) );
    fileQuitAction->setText( tr( "Quit" ) );
    midpointEnableAction->setText( tr( "Action" ) );
    new_menuUnnamedAction->setText( tr( "Unnamed" ) );
    toolsmidpoint_toolAction->setText( tr( "Midpoint" ) );
    toolsmidpoint_toolAction->setToolTip( tr( "Midpoint" ) );
    videoDisplay_Cross_HairAction->setText( tr( "Display Cross Hair" ) );
    videoDisplay_Scale_BarAction->setText( tr( "Display Scale Bar" ) );
    toolsClickMoveAction->setText( tr( "Click and Move" ) );
    toolsCrosshair_ToolAction->setText( tr( "Crosshair" ) );
    toolsCrosshair_ToolAction->setMenuText( tr( "Crosshair" ) );
    toolsCrosshair_ToolAction->setToolTip( tr( "Crosshair - Staff Only!" ) );
    MenuBar->findItem( 0 )->setText( tr( "File" ) );
    MenuBar->findItem( 1 )->setText( tr( "&Display" ) );
    MenuBar->findItem( 2 )->setText( tr( "&Admin" ) );
}

