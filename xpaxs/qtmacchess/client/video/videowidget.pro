SOURCES	+= main.cpp \
	video.c \
	videorenderer.cpp \
	../datasource.cpp
HEADERS	+= video.h \
	videorenderer.h \
	../datasource.h
unix {
  UI_DIR = .ui
  MOC_DIR = .moc
  OBJECTS_DIR = .obj
}
FORMS	= videowidget.ui
TEMPLATE	=app
CONFIG	+= qt warn_on release
DEFINES	+= QT_THREAD_SUPPORT
LIBS	+= -lqt-mt -ljpeg -lImlib -lXv ../libxvidcore.a
LANGUAGE	= C++
