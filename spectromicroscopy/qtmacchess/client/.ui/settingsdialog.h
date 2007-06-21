/****************************************************************************
** Form interface generated from reading ui file 'settingsdialog.ui'
**
** Created: Sat Nov 6 11:56:55 2004
**      by: The User Interface Compiler ($Id: qt/main.cpp   3.1.2   edited Dec 19 11:45 $)
**
** WARNING! All changes made in this file will be lost!
****************************************************************************/

#ifndef SETTINGSDIALOG_H
#define SETTINGSDIALOG_H

#include <qvariant.h>
#include <qdialog.h>

class QVBoxLayout;
class QHBoxLayout;
class QGridLayout;
class QButtonGroup;
class QLabel;
class QLineEdit;
class QComboBox;
class QSpinBox;
class QFrame;
class QPushButton;

class SettingsDialog : public QDialog
{
    Q_OBJECT

public:
    SettingsDialog( QWidget* parent = 0, const char* name = 0, bool modal = FALSE, WFlags fl = 0 );
    ~SettingsDialog();

    QButtonGroup* motorSettingButtonGroup;
    QLabel* MotorIPLabel;
    QLineEdit* motorIPAdressLineEdit;
    QLabel* motorPortLabel;
    QLineEdit* motorPortLineEdit;
    QButtonGroup* videoSettingsButtonGroup;
    QLabel* videoIPLabel;
    QComboBox* resolutionComboBox;
    QLabel* resolutionLabel;
    QLabel* labelBitrate;
    QLabel* qualityLabel;
    QSpinBox* bitrateSpinBox;
    QLabel* kbpsLabel;
    QComboBox* qualityComboBox;
    QLabel* videoPortLabel;
    QLineEdit* videoPortLineEdit;
    QFrame* videoLine;
    QLineEdit* videoIPAddressLineEdit;
    QPushButton* cancelPushButton;
    QPushButton* okPushButton;

protected:

protected slots:
    virtual void languageChange();

private:
    void init();

};

#endif // SETTINGSDIALOG_H
