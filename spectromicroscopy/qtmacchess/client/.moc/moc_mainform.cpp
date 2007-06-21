/****************************************************************************
** MainForm meta object code from reading C++ file 'mainform.h'
**
** Created: Sat Nov 6 11:57:42 2004
**      by: The Qt MOC ($Id: qt/moc_yacc.cpp   3.1.2   edited Feb 24 09:29 $)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#undef QT_NO_COMPAT
#include "../.ui/mainform.h"
#include <qmetaobject.h>
#include <qapplication.h>

#include <private/qucomextra_p.h>
#if !defined(Q_MOC_OUTPUT_REVISION) || (Q_MOC_OUTPUT_REVISION != 26)
#error "This file was generated using the moc from 3.1.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

const char *MainForm::className() const
{
    return "MainForm";
}

QMetaObject *MainForm::metaObj = 0;
static QMetaObjectCleanUp cleanUp_MainForm( "MainForm", &MainForm::staticMetaObject );

#ifndef QT_NO_TRANSLATION
QString MainForm::tr( const char *s, const char *c )
{
    if ( qApp )
	return qApp->translate( "MainForm", s, c, QApplication::DefaultCodec );
    else
	return QString::fromLatin1( s );
}
#ifndef QT_NO_TRANSLATION_UTF8
QString MainForm::trUtf8( const char *s, const char *c )
{
    if ( qApp )
	return qApp->translate( "MainForm", s, c, QApplication::UnicodeUTF8 );
    else
	return QString::fromUtf8( s );
}
#endif // QT_NO_TRANSLATION_UTF8

#endif // QT_NO_TRANSLATION

QMetaObject* MainForm::staticMetaObject()
{
    if ( metaObj )
	return metaObj;
    QMetaObject* parentObject = QMainWindow::staticMetaObject();
    static const QUMethod slot_0 = {"updateCurrentZF", 0, 0 };
    static const QUMethod slot_1 = {"saveSnapshot", 0, 0 };
    static const QUMethod slot_2 = {"multiServerConnect", 0, 0 };
    static const QUMethod slot_3 = {"videoConnected", 0, 0 };
    static const QUParameter param_slot_4[] = {
	{ "value", &static_QUType_int, 0, QUParameter::In }
    };
    static const QUMethod slot_4 = {"moveZoom", 1, param_slot_4 };
    static const QUParameter param_slot_5[] = {
	{ "value", &static_QUType_int, 0, QUParameter::In }
    };
    static const QUMethod slot_5 = {"moveFocus", 1, param_slot_5 };
    static const QUMethod slot_6 = {"motorDisconnect", 0, 0 };
    static const QUMethod slot_7 = {"socketConnected", 0, 0 };
    static const QUMethod slot_8 = {"socketConnectionClosed", 0, 0 };
    static const QUMethod slot_9 = {"socketReadyRead", 0, 0 };
    static const QUMethod slot_10 = {"trev", 0, 0 };
    static const QUMethod slot_11 = {"clickAndMove", 0, 0 };
    static const QUParameter param_slot_12[] = {
	{ "x", &static_QUType_ptr, "float", QUParameter::In },
	{ "y", &static_QUType_ptr, "float", QUParameter::In }
    };
    static const QUMethod slot_12 = {"clickAndMoveMotors", 2, param_slot_12 };
    static const QUMethod slot_13 = {"upButton", 0, 0 };
    static const QUMethod slot_14 = {"downButton", 0, 0 };
    static const QUMethod slot_15 = {"rightButton", 0, 0 };
    static const QUMethod slot_16 = {"leftButton", 0, 0 };
    static const QUMethod slot_17 = {"rotateNinetyButton", 0, 0 };
    static const QUMethod slot_18 = {"rotateOneEightyButton", 0, 0 };
    static const QUMethod slot_19 = {"rotateNegativeNinetyButton", 0, 0 };
    static const QUMethod slot_20 = {"rotateNegativeFiveButton", 0, 0 };
    static const QUMethod slot_21 = {"rotateFiveButton", 0, 0 };
    static const QUMethod slot_22 = {"rotateFortyFiveButton", 0, 0 };
    static const QUMethod slot_23 = {"rotateNegativeFortyFiveButton", 0, 0 };
    static const QUMethod slot_24 = {"rotateZeroButton", 0, 0 };
    static const QUMethod slot_25 = {"updatePhiLineEdit", 0, 0 };
    static const QUMethod slot_26 = {"showSettingsDialog", 0, 0 };
    static const QUMethod slot_27 = {"distanceSliderChanged", 0, 0 };
    static const QUParameter param_slot_28[] = {
	{ "value", &static_QUType_int, 0, QUParameter::In }
    };
    static const QUMethod slot_28 = {"zoomSliderChanged", 1, param_slot_28 };
    static const QUMethod slot_29 = {"distanceLineEditChanged", 0, 0 };
    static const QUParameter param_slot_30[] = {
	{ 0, &static_QUType_ptr, "QObject", QUParameter::In }
    };
    static const QUMethod slot_30 = {"fileSame_ImageAction_destroyed", 1, param_slot_30 };
    static const QUMethod slot_31 = {"inButton", 0, 0 };
    static const QUMethod slot_32 = {"outButton", 0, 0 };
    static const QUMethod slot_33 = {"smallRotFw", 0, 0 };
    static const QUMethod slot_34 = {"smallRotBk", 0, 0 };
    static const QUMethod slot_35 = {"bigRotFw", 0, 0 };
    static const QUMethod slot_36 = {"bigRotBk", 0, 0 };
    static const QUParameter param_slot_37[] = {
	{ "e", &static_QUType_ptr, "QMouseEvent", QUParameter::In }
    };
    static const QUMethod slot_37 = {"movePinOnClick", 1, param_slot_37 };
    static const QUMethod slot_38 = {"rotateThreeSixtyButton", 0, 0 };
    static const QUMethod slot_39 = {"syncAngle", 0, 0 };
    static const QUMethod slot_40 = {"languageChange", 0, 0 };
    static const QMetaData slot_tbl[] = {
	{ "updateCurrentZF()", &slot_0, QMetaData::Public },
	{ "saveSnapshot()", &slot_1, QMetaData::Public },
	{ "multiServerConnect()", &slot_2, QMetaData::Public },
	{ "videoConnected()", &slot_3, QMetaData::Public },
	{ "moveZoom(int)", &slot_4, QMetaData::Public },
	{ "moveFocus(int)", &slot_5, QMetaData::Public },
	{ "motorDisconnect()", &slot_6, QMetaData::Public },
	{ "socketConnected()", &slot_7, QMetaData::Public },
	{ "socketConnectionClosed()", &slot_8, QMetaData::Public },
	{ "socketReadyRead()", &slot_9, QMetaData::Public },
	{ "trev()", &slot_10, QMetaData::Public },
	{ "clickAndMove()", &slot_11, QMetaData::Public },
	{ "clickAndMoveMotors(float,float)", &slot_12, QMetaData::Public },
	{ "upButton()", &slot_13, QMetaData::Public },
	{ "downButton()", &slot_14, QMetaData::Public },
	{ "rightButton()", &slot_15, QMetaData::Public },
	{ "leftButton()", &slot_16, QMetaData::Public },
	{ "rotateNinetyButton()", &slot_17, QMetaData::Public },
	{ "rotateOneEightyButton()", &slot_18, QMetaData::Public },
	{ "rotateNegativeNinetyButton()", &slot_19, QMetaData::Public },
	{ "rotateNegativeFiveButton()", &slot_20, QMetaData::Public },
	{ "rotateFiveButton()", &slot_21, QMetaData::Public },
	{ "rotateFortyFiveButton()", &slot_22, QMetaData::Public },
	{ "rotateNegativeFortyFiveButton()", &slot_23, QMetaData::Public },
	{ "rotateZeroButton()", &slot_24, QMetaData::Public },
	{ "updatePhiLineEdit()", &slot_25, QMetaData::Public },
	{ "showSettingsDialog()", &slot_26, QMetaData::Public },
	{ "distanceSliderChanged()", &slot_27, QMetaData::Public },
	{ "zoomSliderChanged(int)", &slot_28, QMetaData::Public },
	{ "distanceLineEditChanged()", &slot_29, QMetaData::Public },
	{ "fileSame_ImageAction_destroyed(QObject*)", &slot_30, QMetaData::Public },
	{ "inButton()", &slot_31, QMetaData::Public },
	{ "outButton()", &slot_32, QMetaData::Public },
	{ "smallRotFw()", &slot_33, QMetaData::Public },
	{ "smallRotBk()", &slot_34, QMetaData::Public },
	{ "bigRotFw()", &slot_35, QMetaData::Public },
	{ "bigRotBk()", &slot_36, QMetaData::Public },
	{ "movePinOnClick(QMouseEvent*)", &slot_37, QMetaData::Public },
	{ "rotateThreeSixtyButton()", &slot_38, QMetaData::Public },
	{ "syncAngle()", &slot_39, QMetaData::Public },
	{ "languageChange()", &slot_40, QMetaData::Protected }
    };
    metaObj = QMetaObject::new_metaobject(
	"MainForm", parentObject,
	slot_tbl, 41,
	0, 0,
#ifndef QT_NO_PROPERTIES
	0, 0,
	0, 0,
#endif // QT_NO_PROPERTIES
	0, 0 );
    cleanUp_MainForm.setMetaObject( metaObj );
    return metaObj;
}

void* MainForm::qt_cast( const char* clname )
{
    if ( !qstrcmp( clname, "MainForm" ) )
	return this;
    return QMainWindow::qt_cast( clname );
}

bool MainForm::qt_invoke( int _id, QUObject* _o )
{
    switch ( _id - staticMetaObject()->slotOffset() ) {
    case 0: updateCurrentZF(); break;
    case 1: saveSnapshot(); break;
    case 2: multiServerConnect(); break;
    case 3: videoConnected(); break;
    case 4: moveZoom((int)static_QUType_int.get(_o+1)); break;
    case 5: moveFocus((int)static_QUType_int.get(_o+1)); break;
    case 6: motorDisconnect(); break;
    case 7: socketConnected(); break;
    case 8: socketConnectionClosed(); break;
    case 9: socketReadyRead(); break;
    case 10: trev(); break;
    case 11: clickAndMove(); break;
    case 12: clickAndMoveMotors((float)(*((float*)static_QUType_ptr.get(_o+1))),(float)(*((float*)static_QUType_ptr.get(_o+2)))); break;
    case 13: upButton(); break;
    case 14: downButton(); break;
    case 15: rightButton(); break;
    case 16: leftButton(); break;
    case 17: rotateNinetyButton(); break;
    case 18: rotateOneEightyButton(); break;
    case 19: rotateNegativeNinetyButton(); break;
    case 20: rotateNegativeFiveButton(); break;
    case 21: rotateFiveButton(); break;
    case 22: rotateFortyFiveButton(); break;
    case 23: rotateNegativeFortyFiveButton(); break;
    case 24: rotateZeroButton(); break;
    case 25: updatePhiLineEdit(); break;
    case 26: showSettingsDialog(); break;
    case 27: distanceSliderChanged(); break;
    case 28: zoomSliderChanged((int)static_QUType_int.get(_o+1)); break;
    case 29: distanceLineEditChanged(); break;
    case 30: fileSame_ImageAction_destroyed((QObject*)static_QUType_ptr.get(_o+1)); break;
    case 31: inButton(); break;
    case 32: outButton(); break;
    case 33: smallRotFw(); break;
    case 34: smallRotBk(); break;
    case 35: bigRotFw(); break;
    case 36: bigRotBk(); break;
    case 37: movePinOnClick((QMouseEvent*)static_QUType_ptr.get(_o+1)); break;
    case 38: rotateThreeSixtyButton(); break;
    case 39: syncAngle(); break;
    case 40: languageChange(); break;
    default:
	return QMainWindow::qt_invoke( _id, _o );
    }
    return TRUE;
}

bool MainForm::qt_emit( int _id, QUObject* _o )
{
    return QMainWindow::qt_emit(_id,_o);
}
#ifndef QT_NO_PROPERTIES

bool MainForm::qt_property( int id, int f, QVariant* v)
{
    return QMainWindow::qt_property( id, f, v);
}

bool MainForm::qt_static_property( QObject* , int , int , QVariant* ){ return FALSE; }
#endif // QT_NO_PROPERTIES
