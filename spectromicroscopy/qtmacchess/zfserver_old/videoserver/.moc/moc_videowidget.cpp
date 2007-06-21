/****************************************************************************
** VideoWidget meta object code from reading C++ file 'videowidget.h'
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#undef QT_NO_COMPAT
#include "../.ui/videowidget.h"
#include <qmetaobject.h>
#include <qapplication.h>

#include <private/qucomextra_p.h>
#if !defined(Q_MOC_OUTPUT_REVISION) || (Q_MOC_OUTPUT_REVISION != 26)
#error "This file was generated using the moc from 3.1.1. It"
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
    static const QUMethod slot_0 = {"toggleSocket", 0, 0 };
    static const QUParameter param_slot_1[] = {
	{ "x", &static_QUType_int, 0, QUParameter::In },
	{ "y", &static_QUType_int, 0, QUParameter::In }
    };
    static const QUMethod slot_1 = {"setCrossHair", 2, param_slot_1 };
    static const QUParameter param_slot_2[] = {
	{ "e", &static_QUType_ptr, "QMouseEvent", QUParameter::In }
    };
    static const QUMethod slot_2 = {"mouseDoubleClickEvent", 1, param_slot_2 };
    static const QUParameter param_slot_3[] = {
	{ "hostname", &static_QUType_QString, 0, QUParameter::In },
	{ "ipAddress", &static_QUType_QString, 0, QUParameter::In }
    };
    static const QUMethod slot_3 = {"addClientToTable", 2, param_slot_3 };
    static const QUParameter param_slot_4[] = {
	{ "ipAddress", &static_QUType_QString, 0, QUParameter::In }
    };
    static const QUMethod slot_4 = {"remClientFromTable", 1, param_slot_4 };
    static const QUMethod slot_5 = {"updateEnc", 0, 0 };
    static const QUMethod slot_6 = {"updateUptime", 0, 0 };
    static const QUMethod slot_7 = {"languageChange", 0, 0 };
    static const QMetaData slot_tbl[] = {
	{ "toggleSocket()", &slot_0, QMetaData::Public },
	{ "setCrossHair(int,int)", &slot_1, QMetaData::Public },
	{ "mouseDoubleClickEvent(QMouseEvent*)", &slot_2, QMetaData::Public },
	{ "addClientToTable(QString,QString)", &slot_3, QMetaData::Public },
	{ "remClientFromTable(QString)", &slot_4, QMetaData::Public },
	{ "updateEnc()", &slot_5, QMetaData::Public },
	{ "updateUptime()", &slot_6, QMetaData::Public },
	{ "languageChange()", &slot_7, QMetaData::Protected }
    };
    metaObj = QMetaObject::new_metaobject(
	"VideoWidget", parentObject,
	slot_tbl, 8,
	0, 0,
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

bool VideoWidget::qt_invoke( int _id, QUObject* _o )
{
    switch ( _id - staticMetaObject()->slotOffset() ) {
    case 0: toggleSocket(); break;
    case 1: setCrossHair((int)static_QUType_int.get(_o+1),(int)static_QUType_int.get(_o+2)); break;
    case 2: mouseDoubleClickEvent((QMouseEvent*)static_QUType_ptr.get(_o+1)); break;
    case 3: addClientToTable((QString)static_QUType_QString.get(_o+1),(QString)static_QUType_QString.get(_o+2)); break;
    case 4: remClientFromTable((QString)static_QUType_QString.get(_o+1)); break;
    case 5: updateEnc(); break;
    case 6: updateUptime(); break;
    case 7: languageChange(); break;
    default:
	return QWidget::qt_invoke( _id, _o );
    }
    return TRUE;
}

bool VideoWidget::qt_emit( int _id, QUObject* _o )
{
    return QWidget::qt_emit(_id,_o);
}
#ifndef QT_NO_PROPERTIES

bool VideoWidget::qt_property( int id, int f, QVariant* v)
{
    return QWidget::qt_property( id, f, v);
}

bool VideoWidget::qt_static_property( QObject* , int , int , QVariant* ){ return FALSE; }
#endif // QT_NO_PROPERTIES
