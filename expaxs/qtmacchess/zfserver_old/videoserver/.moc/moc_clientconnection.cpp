/****************************************************************************
** ClientConnection meta object code from reading C++ file 'clientconnection.h'
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#undef QT_NO_COMPAT
#include "../clientconnection.h"
#include <qmetaobject.h>
#include <qapplication.h>

#include <private/qucomextra_p.h>
#if !defined(Q_MOC_OUTPUT_REVISION) || (Q_MOC_OUTPUT_REVISION != 26)
#error "This file was generated using the moc from 3.1.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

const char *ClientConnection::className() const
{
    return "ClientConnection";
}

QMetaObject *ClientConnection::metaObj = 0;
static QMetaObjectCleanUp cleanUp_ClientConnection( "ClientConnection", &ClientConnection::staticMetaObject );

#ifndef QT_NO_TRANSLATION
QString ClientConnection::tr( const char *s, const char *c )
{
    if ( qApp )
	return qApp->translate( "ClientConnection", s, c, QApplication::DefaultCodec );
    else
	return QString::fromLatin1( s );
}
#ifndef QT_NO_TRANSLATION_UTF8
QString ClientConnection::trUtf8( const char *s, const char *c )
{
    if ( qApp )
	return qApp->translate( "ClientConnection", s, c, QApplication::UnicodeUTF8 );
    else
	return QString::fromUtf8( s );
}
#endif // QT_NO_TRANSLATION_UTF8

#endif // QT_NO_TRANSLATION

QMetaObject* ClientConnection::staticMetaObject()
{
    if ( metaObj )
	return metaObj;
    QMetaObject* parentObject = QSocket::staticMetaObject();
    static const QUMethod slot_0 = {"readClient", 0, 0 };
    static const QUMethod slot_1 = {"terminateConnection", 0, 0 };
    static const QMetaData slot_tbl[] = {
	{ "readClient()", &slot_0, QMetaData::Public },
	{ "terminateConnection()", &slot_1, QMetaData::Public }
    };
    static const QUParameter param_signal_0[] = {
	{ "s", &static_QUType_ptr, "ClientConnection", QUParameter::In }
    };
    static const QUMethod signal_0 = {"clientSocketClosed", 1, param_signal_0 };
    static const QMetaData signal_tbl[] = {
	{ "clientSocketClosed(ClientConnection*)", &signal_0, QMetaData::Public }
    };
    metaObj = QMetaObject::new_metaobject(
	"ClientConnection", parentObject,
	slot_tbl, 2,
	signal_tbl, 1,
#ifndef QT_NO_PROPERTIES
	0, 0,
	0, 0,
#endif // QT_NO_PROPERTIES
	0, 0 );
    cleanUp_ClientConnection.setMetaObject( metaObj );
    return metaObj;
}

void* ClientConnection::qt_cast( const char* clname )
{
    if ( !qstrcmp( clname, "ClientConnection" ) )
	return this;
    return QSocket::qt_cast( clname );
}

#include <qobjectdefs.h>
#include <qsignalslotimp.h>

// SIGNAL clientSocketClosed
void ClientConnection::clientSocketClosed( ClientConnection* t0 )
{
    if ( signalsBlocked() )
	return;
    QConnectionList *clist = receivers( staticMetaObject()->signalOffset() + 0 );
    if ( !clist )
	return;
    QUObject o[2];
    static_QUType_ptr.set(o+1,t0);
    activate_signal( clist, o );
}

bool ClientConnection::qt_invoke( int _id, QUObject* _o )
{
    switch ( _id - staticMetaObject()->slotOffset() ) {
    case 0: readClient(); break;
    case 1: terminateConnection(); break;
    default:
	return QSocket::qt_invoke( _id, _o );
    }
    return TRUE;
}

bool ClientConnection::qt_emit( int _id, QUObject* _o )
{
    switch ( _id - staticMetaObject()->signalOffset() ) {
    case 0: clientSocketClosed((ClientConnection*)static_QUType_ptr.get(_o+1)); break;
    default:
	return QSocket::qt_emit(_id,_o);
    }
    return TRUE;
}
#ifndef QT_NO_PROPERTIES

bool ClientConnection::qt_property( int id, int f, QVariant* v)
{
    return QSocket::qt_property( id, f, v);
}

bool ClientConnection::qt_static_property( QObject* , int , int , QVariant* ){ return FALSE; }
#endif // QT_NO_PROPERTIES
