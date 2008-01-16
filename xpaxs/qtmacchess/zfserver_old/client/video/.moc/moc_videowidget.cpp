/****************************************************************************
** VideoWidget meta object code from reading C++ file 'videowidget.h'
**
** Created: Mon Mar 1 16:45:06 2004
**      by: The Qt MOC ($Id: moc_videowidget.cpp,v 1.1.1.1 2004/05/26 18:32:22 degani Exp $)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#undef QT_NO_COMPAT
#include "../.ui/videowidget.h"
#include <qmetaobject.h>
#include <qapplication.h>

#include <private/qucomextra_p.h>
#if !defined(Q_MOC_OUTPUT_REVISION) || (Q_MOC_OUTPUT_REVISION != 26)
#error "This file was generated using the moc from 3.2.0. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

const char *VideoWidget::className() const
{
    return "VideoWidget";
}

QMetaObject *VideoWidget::metaObj = 0;
static QMetaObjectCleanUp cleanUp_VideoWidget( "VideoWidget", &VideoWidget::staticMetaObject );

#ifndef QT_NO_TRANSLATION
QString VideoWidget::tr( const char *s, const char *c )
{
    if ( qApp )
	return qApp->translate( "VideoWidget", s, c, QApplication::DefaultCodec );
    else
	return QString::fromLatin1( s );
}
#ifndef QT_NO_TRANSLATION_UTF8
QString VideoWidget::trUtf8( const char *s, const char *c )
{
    if ( qApp )
	return qApp->translate( "VideoWidget", s, c, QApplication::UnicodeUTF8 );
    else
	return QString::fromUtf8( s );
}
#endif // QT_NO_TRANSLATION_UTF8

#endif // QT_NO_TRANSLATION

QMetaObject* VideoWidget::staticMetaObject()
{
    if ( metaObj )
	return metaObj;
    QMetaObject* parentObject = QWidget::staticMetaObject();
    static const QUMethod slot_0 = {"saveImage", 0, 0 };
    static const QUMethod slot_1 = {"start", 0, 0 };
    static const QUMethod slot_2 = {"stop", 0, 0 };
    static const QUParameter param_slot_3[] = {
	{ "x", &static_QUType_int, 0, QUParameter::In },
	{ "y", &static_QUType_int, 0, QUParameter::In }
    };
    static const QUMethod slot_3 = {"setCrossHair", 2, param_slot_3 };
    static const QUParameter param_slot_4[] = {
	{ "e", &static_QUType_ptr, "QMouseEvent", QUParameter::In }
    };
    static const QUMethod slot_4 = {"mouseDoubleClickEvent", 1, param_slot_4 };
    static const QUParameter param_slot_5[] = {
	{ "a", &static_QUType_bool, 0, QUParameter::In }
    };
    static const QUMethod slot_5 = {"setCrossHairEnabled", 1, param_slot_5 };
    static const QUParameter param_slot_6[] = {
	{ "a", &static_QUType_bool, 0, QUParameter::In }
    };
    static const QUMethod slot_6 = {"midpointEnabled", 1, param_slot_6 };
    static const QUParameter param_slot_7[] = {
	{ "a", &static_QUType_bool, 0, QUParameter::In }
    };
    static const QUMethod slot_7 = {"crossHairDisplayed", 1, param_slot_7 };
    static const QUParameter param_slot_8[] = {
	{ "e", &static_QUType_ptr, "QMouseEvent", QUParameter::In }
    };
    static const QUMethod slot_8 = {"mouseReleaseEvent", 1, param_slot_8 };
    static const QUParameter param_slot_9[] = {
	{ "a", &static_QUType_bool, 0, QUParameter::In }
    };
    static const QUMethod slot_9 = {"scaleBarDisplayed", 1, param_slot_9 };
    static const QUMethod slot_10 = {"languageChange", 0, 0 };
    static const QMetaData slot_tbl[] = {
	{ "saveImage()", &slot_0, QMetaData::Public },
	{ "start()", &slot_1, QMetaData::Public },
	{ "stop()", &slot_2, QMetaData::Public },
	{ "setCrossHair(int,int)", &slot_3, QMetaData::Public },
	{ "mouseDoubleClickEvent(QMouseEvent*)", &slot_4, QMetaData::Public },
	{ "setCrossHairEnabled(bool)", &slot_5, QMetaData::Public },
	{ "midpointEnabled(bool)", &slot_6, QMetaData::Public },
	{ "crossHairDisplayed(bool)", &slot_7, QMetaData::Public },
	{ "mouseReleaseEvent(QMouseEvent*)", &slot_8, QMetaData::Public },
	{ "scaleBarDisplayed(bool)", &slot_9, QMetaData::Public },
	{ "languageChange()", &slot_10, QMetaData::Protected }
    };
    static const QUMethod signal_0 = {"videoConnected", 0, 0 };
    static const QUParameter param_signal_1[] = {
	{ 0, &static_QUType_ptr, "float", QUParameter::In },
	{ 0, &static_QUType_ptr, "float", QUParameter::In }
    };
    static const QUMethod signal_1 = {"clickAndMoveMotors", 2, param_signal_1 };
    static const QMetaData signal_tbl[] = {
	{ "videoConnected()", &signal_0, QMetaData::Public },
	{ "clickAndMoveMotors(float,float)", &signal_1, QMetaData::Public }
    };
    metaObj = QMetaObject::new_metaobject(
	"VideoWidget", parentObject,
	slot_tbl, 11,
	signal_tbl, 2,
#ifndef QT_NO_PROPERTIES
	0, 0,
	0, 0,
#endif // QT_NO_PROPERTIES
	0, 0 );
    cleanUp_VideoWidget.setMetaObject( metaObj );
    return metaObj;
}

void* VideoWidget::qt_cast( const char* clname )
{
    if ( !qstrcmp( clname, "VideoWidget" ) )
	return this;
    return QWidget::qt_cast( clname );
}

// SIGNAL videoConnected
void VideoWidget::videoConnected()
{
    activate_signal( staticMetaObject()->signalOffset() + 0 );
}

#include <qobjectdefs.h>
#include <qsignalslotimp.h>

// SIGNAL clickAndMoveMotors
void VideoWidget::clickAndMoveMotors( float t0, float t1 )
{
    if ( signalsBlocked() )
	return;
    QConnectionList *clist = receivers( staticMetaObject()->signalOffset() + 1 );
    if ( !clist )
	return;
    QUObject o[3];
    static_QUType_ptr.set(o+1,&t0);
    static_QUType_ptr.set(o+2,&t1);
    activate_signal( clist, o );
}

bool VideoWidget::qt_invoke( int _id, QUObject* _o )
{
    switch ( _id - staticMetaObject()->slotOffset() ) {
    case 0: saveImage(); break;
    case 1: start(); break;
    case 2: stop(); break;
    case 3: setCrossHair((int)static_QUType_int.get(_o+1),(int)static_QUType_int.get(_o+2)); break;
    case 4: mouseDoubleClickEvent((QMouseEvent*)static_QUType_ptr.get(_o+1)); break;
    case 5: setCrossHairEnabled((bool)static_QUType_bool.get(_o+1)); break;
    case 6: midpointEnabled((bool)static_QUType_bool.get(_o+1)); break;
    case 7: crossHairDisplayed((bool)static_QUType_bool.get(_o+1)); break;
    case 8: mouseReleaseEvent((QMouseEvent*)static_QUType_ptr.get(_o+1)); break;
    case 9: scaleBarDisplayed((bool)static_QUType_bool.get(_o+1)); break;
    case 10: languageChange(); break;
    default:
	return QWidget::qt_invoke( _id, _o );
    }
    return TRUE;
}

bool VideoWidget::qt_emit( int _id, QUObject* _o )
{
    switch ( _id - staticMetaObject()->signalOffset() ) {
    case 0: videoConnected(); break;
    case 1: clickAndMoveMotors((float)(*((float*)static_QUType_ptr.get(_o+1))),(float)(*((float*)static_QUType_ptr.get(_o+2)))); break;
    default:
	return QWidget::qt_emit(_id,_o);
    }
    return TRUE;
}
#ifndef QT_NO_PROPERTIES

bool VideoWidget::qt_property( int id, int f, QVariant* v)
{
    return QWidget::qt_property( id, f, v);
}

bool VideoWidget::qt_static_property( QObject* , int , int , QVariant* ){ return FALSE; }
#endif // QT_NO_PROPERTIES
