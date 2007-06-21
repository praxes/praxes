TEMPLATE	= app
LANGUAGE	= C++

CONFIG	+= qt warn_on release

LIBS	+= -lqt-mt -lXv /usr/local/lib/libxvidcore.a -lraw1394 -ldc1394_control

DEFINES	+= QT_THREAD_SUPPORT

HEADERS	+= video.h \
	driver.h \
	videorenderer.h \
	videoserver.h \
	clientconnection.h

SOURCES	+= main.cpp \
	video.c \
	driver.c \
	videorenderer.cpp \
	videoserver.cpp \
	clientconnection.cpp

FORMS	= videowidget.ui

unix {
  UI_DIR = .ui
  MOC_DIR = .moc
  OBJECTS_DIR = .obj
}
