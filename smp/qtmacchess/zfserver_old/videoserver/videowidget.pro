SOURCES	+= main.cpp \
	video.c \
	driver.c \
	videorenderer.cpp \
	videoserver.cpp \
	clientconnection.cpp
HEADERS	+= video.h \
	driver.h \
	videorenderer.h \
	videoserver.h \
	clientconnection.h
unix {
  UI_DIR = .ui
  MOC_DIR = .moc
  OBJECTS_DIR = .obj
}
FORMS	= videowidget.ui
TEMPLATE	=app
CONFIG	+= qt warn_on release
DEFINES	+= QT_THREAD_SUPPORT
LIBS	+= -lqt-mt -lXv /usr/local/lib/libxvidcore.a -lraw1394 -ldc1394_control
LANGUAGE	= C++
