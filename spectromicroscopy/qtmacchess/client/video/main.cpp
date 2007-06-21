#include <qapplication.h>
#include "videowidget.h"

int main( int argc, char ** argv )
{
    QApplication a( argc, argv );
    VideoWidget w;
    w.show();
    a.connect( &a, SIGNAL( lastWindowClosed() ), &a, SLOT( quit() ) );
    return a.exec();
}
