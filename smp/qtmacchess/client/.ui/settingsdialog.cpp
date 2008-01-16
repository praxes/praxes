/****************************************************************************
** Form implementation generated from reading ui file 'settingsdialog.ui'
**
** Created: Sat Nov 6 11:57:27 2004
**      by: The User Interface Compiler ($Id: qt/main.cpp   3.1.2   edited Dec 19 11:45 $)
**
** WARNING! All changes made in this file will be lost!
****************************************************************************/

#include "settingsdialog.h"

#include <qvariant.h>
#include <qbuttongroup.h>
#include <qlabel.h>
#include <qlineedit.h>
#include <qcombobox.h>
#include <qspinbox.h>
#include <qframe.h>
#include <qpushbutton.h>
#include <qlayout.h>
#include <qtooltip.h>
#include <qwhatsthis.h>
#include <qimage.h>
#include <qpixmap.h>

#include "../settingsdialog.ui.h"
/* 
 *  Constructs a SettingsDialog as a child of 'parent', with the 
 *  name 'name' and widget flags set to 'f'.
 *
 *  The dialog will by default be modeless, unless you set 'modal' to
 *  TRUE to construct a modal dialog.
 */
SettingsDialog::SettingsDialog( QWidget* parent, const char* name, bool modal, WFlags fl )
    : QDialog( parent, name, modal, fl )
{
    if ( !name )
	setName( "SettingsDialog" );

    motorSettingButtonGroup = new QButtonGroup( this, "motorSettingButtonGroup" );
    motorSettingButtonGroup->setGeometry( QRect( 390, 10, 160, 130 ) );

    MotorIPLabel = new QLabel( motorSettingButtonGroup, "MotorIPLabel" );
    MotorIPLabel->setGeometry( QRect( 10, 30, 140, 20 ) );

    motorIPAdressLineEdit = new QLineEdit( motorSettingButtonGroup, "motorIPAdressLineEdit" );
    motorIPAdressLineEdit->setGeometry( QRect( 10, 60, 140, 22 ) );

    motorPortLabel = new QLabel( motorSettingButtonGroup, "motorPortLabel" );
    motorPortLabel->setGeometry( QRect( 10, 90, 57, 20 ) );

    motorPortLineEdit = new QLineEdit( motorSettingButtonGroup, "motorPortLineEdit" );
    motorPortLineEdit->setGeometry( QRect( 100, 90, 50, 22 ) );

    videoSettingsButtonGroup = new QButtonGroup( this, "videoSettingsButtonGroup" );
    videoSettingsButtonGroup->setGeometry( QRect( 10, 10, 370, 130 ) );

    videoIPLabel = new QLabel( videoSettingsButtonGroup, "videoIPLabel" );
    videoIPLabel->setGeometry( QRect( 20, 30, 140, 20 ) );

    resolutionComboBox = new QComboBox( FALSE, videoSettingsButtonGroup, "resolutionComboBox" );
    resolutionComboBox->setGeometry( QRect( 250, 30, 90, 22 ) );

    resolutionLabel = new QLabel( videoSettingsButtonGroup, "resolutionLabel" );
    resolutionLabel->setGeometry( QRect( 180, 30, 65, 20 ) );

    labelBitrate = new QLabel( videoSettingsButtonGroup, "labelBitrate" );
    labelBitrate->setGeometry( QRect( 180, 60, 50, 20 ) );

    qualityLabel = new QLabel( videoSettingsButtonGroup, "qualityLabel" );
    qualityLabel->setGeometry( QRect( 180, 90, 50, 20 ) );

    bitrateSpinBox = new QSpinBox( videoSettingsButtonGroup, "bitrateSpinBox" );
    bitrateSpinBox->setGeometry( QRect( 250, 60, 70, 22 ) );
    bitrateSpinBox->setMaxValue( 10000 );
    bitrateSpinBox->setValue( 900 );

    kbpsLabel = new QLabel( videoSettingsButtonGroup, "kbpsLabel" );
    kbpsLabel->setGeometry( QRect( 330, 60, 30, 20 ) );

    qualityComboBox = new QComboBox( FALSE, videoSettingsButtonGroup, "qualityComboBox" );
    qualityComboBox->setGeometry( QRect( 250, 90, 85, 22 ) );

    videoPortLabel = new QLabel( videoSettingsButtonGroup, "videoPortLabel" );
    videoPortLabel->setGeometry( QRect( 20, 90, 57, 20 ) );

    videoPortLineEdit = new QLineEdit( videoSettingsButtonGroup, "videoPortLineEdit" );
    videoPortLineEdit->setGeometry( QRect( 110, 90, 50, 22 ) );

    videoLine = new QFrame( videoSettingsButtonGroup, "videoLine" );
    videoLine->setGeometry( QRect( 160, 20, 20, 100 ) );
    videoLine->setFrameShape( QFrame::VLine );
    videoLine->setFrameShadow( QFrame::Sunken );
    videoLine->setFrameShape( QFrame::VLine );

    videoIPAddressLineEdit = new QLineEdit( videoSettingsButtonGroup, "videoIPAddressLineEdit" );
    videoIPAddressLineEdit->setGeometry( QRect( 20, 60, 140, 22 ) );

    cancelPushButton = new QPushButton( this, "cancelPushButton" );
    cancelPushButton->setGeometry( QRect( 630, 150, 92, 30 ) );

    okPushButton = new QPushButton( this, "okPushButton" );
    okPushButton->setGeometry( QRect( 530, 150, 92, 30 ) );
    languageChange();
    resize( QSize(750, 199).expandedTo(minimumSizeHint()) );
    clearWState( WState_Polished );

    // signals and slots connections
    connect( okPushButton, SIGNAL( clicked() ), this, SLOT( close() ) );
    connect( cancelPushButton, SIGNAL( clicked() ), this, SLOT( close() ) );
    init();
}

/*
 *  Destroys the object and frees any allocated resources
 */
SettingsDialog::~SettingsDialog()
{
    // no need to delete child widgets, Qt does it all for us
}

/*
 *  Sets the strings of the subwidgets using the current
 *  language.
 */
void SettingsDialog::languageChange()
{
    setCaption( tr( "Settings" ) );
    motorSettingButtonGroup->setTitle( tr( "CompuMotor Settings" ) );
    MotorIPLabel->setText( tr( "IP Address / Hostname:" ) );
    motorPortLabel->setText( tr( "Port:" ) );
    videoSettingsButtonGroup->setTitle( tr( "Video Settings" ) );
    videoIPLabel->setText( tr( "IP Address / Hostname: " ) );
    resolutionComboBox->clear();
    resolutionComboBox->insertItem( tr( "1024 x 768" ) );
    resolutionComboBox->insertItem( tr( "800 x 600" ) );
    resolutionComboBox->insertItem( tr( "640 x 480" ) );
    resolutionComboBox->insertItem( tr( "320 x 240" ) );
    resolutionLabel->setText( tr( "Resolution: " ) );
    labelBitrate->setText( tr( "Bitrate:" ) );
    qualityLabel->setText( tr( "Quality: " ) );
    kbpsLabel->setText( tr( "kbps" ) );
    qualityComboBox->clear();
    qualityComboBox->insertItem( tr( "Very High" ) );
    qualityComboBox->insertItem( tr( "High" ) );
    qualityComboBox->insertItem( tr( "Medium" ) );
    qualityComboBox->insertItem( tr( "Medium Low" ) );
    qualityComboBox->insertItem( tr( "Low" ) );
    videoPortLabel->setText( tr( "Port: " ) );
    cancelPushButton->setText( tr( "Cancel" ) );
    okPushButton->setText( tr( "OK" ) );
}

