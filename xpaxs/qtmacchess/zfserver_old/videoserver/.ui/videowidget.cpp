/****************************************************************************
** Form implementation generated from reading ui file 'videowidget.ui'
**
** Created: Sat Feb 28 21:18:34 2004
**      by: The User Interface Compiler ($Id: videowidget.cpp,v 1.1.1.1 2004/05/26 18:32:22 degani Exp $)
**
** WARNING! All changes made in this file will be lost!
****************************************************************************/

#include "videowidget.h"

#include <qvariant.h>
#include <qbuttongroup.h>
#include <qframe.h>
#include <qlabel.h>
#include <qlineedit.h>
#include <qtable.h>
#include <qlayout.h>
#include <qtooltip.h>
#include <qwhatsthis.h>
#include "../videowidget.ui.h"

/* 
 *  Constructs a VideoWidget as a child of 'parent', with the 
 *  name 'name' and widget flags set to 'f'.
 */
VideoWidget::VideoWidget( QWidget* parent, const char* name, WFlags fl )
    : QWidget( parent, name, fl )
{
    if ( !name )
	setName( "VideoWidget" );
    setMinimumSize( QSize( 1024, 908 ) );
    setPaletteBackgroundColor( QColor( 0, 0, 0 ) );

    controlFrame = new QFrame( this, "controlFrame" );
    controlFrame->setGeometry( QRect( 0, 768, 1024, 140 ) );
    controlFrame->setPaletteBackgroundColor( QColor( 230, 230, 230 ) );
    controlFrame->setFrameShape( QFrame::StyledPanel );
    controlFrame->setFrameShadow( QFrame::Raised );

    clientGroup = new QButtonGroup( controlFrame, "clientGroup" );
    clientGroup->setGeometry( QRect( 5, 3, 396, 130 ) );

    numClients = new QLineEdit( clientGroup, "numClients" );
    numClients->setEnabled( TRUE );
    numClients->setGeometry( QRect( 350, 8, 30, 23 ) );
    numClients->setAlignment( int( QLineEdit::AlignHCenter ) );
    numClients->setReadOnly( TRUE );

    clientLabel = new QLabel( clientGroup, "clientLabel" );
    clientLabel->setGeometry( QRect( 10, 3, 340, 27 ) );
    QFont clientLabel_font(  clientLabel->font() );
    clientLabel_font.setPointSize( 14 );
    clientLabel->setFont( clientLabel_font ); 

    clientTable = new QTable( clientGroup, "clientTable" );
    clientTable->setNumCols( clientTable->numCols() + 1 );
    clientTable->horizontalHeader()->setLabel( clientTable->numCols() - 1, tr( "Hostname" ) );
    clientTable->setNumCols( clientTable->numCols() + 1 );
    clientTable->horizontalHeader()->setLabel( clientTable->numCols() - 1, tr( "IP Address" ) );
    clientTable->setNumCols( clientTable->numCols() + 1 );
    clientTable->horizontalHeader()->setLabel( clientTable->numCols() - 1, tr( "Connection Date" ) );
    clientTable->setGeometry( QRect( 10, 38, 373, 87 ) );
    clientTable->setSizePolicy( QSizePolicy( (QSizePolicy::SizeType)7, (QSizePolicy::SizeType)7, 1, 1, clientTable->sizePolicy().hasHeightForWidth() ) );
    clientTable->setAcceptDrops( FALSE );
    clientTable->setResizePolicy( QTable::Manual );
    clientTable->setVScrollBarMode( QTable::Auto );
    clientTable->setHScrollBarMode( QTable::AlwaysOff );
    clientTable->setNumRows( 0 );
    clientTable->setNumCols( 3 );
    clientTable->setReadOnly( TRUE );
    clientTable->setSelectionMode( QTable::NoSelection );
    clientTable->setFocusStyle( QTable::SpreadSheet );

    xvidGroup = new QButtonGroup( controlFrame, "xvidGroup" );
    xvidGroup->setGeometry( QRect( 411, 3, 290, 130 ) );

    xvidLabel = new QLabel( xvidGroup, "xvidLabel" );
    xvidLabel->setGeometry( QRect( 30, 3, 230, 27 ) );
    QFont xvidLabel_font(  xvidLabel->font() );
    xvidLabel_font.setPointSize( 14 );
    xvidLabel->setFont( xvidLabel_font ); 

    currentFrameLabel = new QLabel( xvidGroup, "currentFrameLabel" );
    currentFrameLabel->setGeometry( QRect( 40, 45, 130, 20 ) );

    compressTimeLabel = new QLabel( xvidGroup, "compressTimeLabel" );
    compressTimeLabel->setGeometry( QRect( 40, 65, 145, 20 ) );

    frameSizeLabel = new QLabel( xvidGroup, "frameSizeLabel" );
    frameSizeLabel->setGeometry( QRect( 40, 85, 130, 20 ) );

    currentFrame = new QLineEdit( xvidGroup, "currentFrame" );
    currentFrame->setEnabled( TRUE );
    currentFrame->setGeometry( QRect( 200, 45, 80, 23 ) );
    currentFrame->setAlignment( int( QLineEdit::AlignRight ) );
    currentFrame->setReadOnly( TRUE );

    compressTime = new QLineEdit( xvidGroup, "compressTime" );
    compressTime->setEnabled( TRUE );
    compressTime->setGeometry( QRect( 200, 65, 80, 23 ) );
    compressTime->setAlignment( int( QLineEdit::AlignRight ) );
    compressTime->setReadOnly( TRUE );

    frameSize = new QLineEdit( xvidGroup, "frameSize" );
    frameSize->setEnabled( TRUE );
    frameSize->setGeometry( QRect( 200, 85, 80, 23 ) );
    frameSize->setAlignment( int( QLineEdit::AlignRight ) );
    frameSize->setReadOnly( TRUE );

    uptimeGroup = new QButtonGroup( controlFrame, "uptimeGroup" );
    uptimeGroup->setGeometry( QRect( 710, 3, 310, 130 ) );

    uptimeLabel = new QLabel( uptimeGroup, "uptimeLabel" );
    uptimeLabel->setGeometry( QRect( 114, 45, 82, 20 ) );

    serverLabel = new QLabel( uptimeGroup, "serverLabel" );
    serverLabel->setGeometry( QRect( 20, 3, 270, 27 ) );
    QFont serverLabel_font(  serverLabel->font() );
    serverLabel_font.setPointSize( 14 );
    serverLabel->setFont( serverLabel_font ); 

    uptime = new QLineEdit( uptimeGroup, "uptime" );
    uptime->setGeometry( QRect( 15, 65, 280, 23 ) );
    uptime->setAlignment( int( QLineEdit::AlignHCenter ) );
    languageChange();
    resize( QSize(1024, 908).expandedTo(minimumSizeHint()) );
    init();
}

/*
 *  Destroys the object and frees any allocated resources
 */
VideoWidget::~VideoWidget()
{
    // no need to delete child widgets, Qt does it all for us
}

/*
 *  Sets the strings of the subwidgets using the current
 *  language.
 */
void VideoWidget::languageChange()
{
    setCaption( tr( "Macchess Digital Streaming Server" ) );
    clientGroup->setTitle( QString::null );
    numClients->setText( tr( "0" ) );
    clientLabel->setText( tr( "Number of clients currently connected:" ) );
    clientTable->horizontalHeader()->setLabel( 0, tr( "Hostname" ) );
    clientTable->horizontalHeader()->setLabel( 1, tr( "IP Address" ) );
    clientTable->horizontalHeader()->setLabel( 2, tr( "Connection Date" ) );
    xvidGroup->setTitle( QString::null );
    xvidLabel->setText( tr( "<p align=\"center\">XVID Encoder Statistics</p>" ) );
    currentFrameLabel->setText( tr( "Current Frame:" ) );
    compressTimeLabel->setText( tr( "Time to Compress (ms):" ) );
    frameSizeLabel->setText( tr( "Size of Frame (bytes):" ) );
    currentFrame->setText( tr( "0" ) );
    compressTime->setText( tr( "0" ) );
    frameSize->setText( tr( "0" ) );
    uptimeGroup->setTitle( QString::null );
    uptimeLabel->setText( tr( "Total Uptime:" ) );
    serverLabel->setText( tr( "<p align=\"center\">Server Statistics</p>" ) );
}

