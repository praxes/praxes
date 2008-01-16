SOURCES	+= main.cpp \
	video/.ui/videowidget.cpp \
	video/video.c \
	video/videorenderer.cpp \
	datasource.cpp \
	zfthread.cpp
HEADERS	+= video/.ui/videowidget.h \
	datasource.h \
	video/video.h \
	video/videorenderer.h \
	zfthread.h
unix {
  UI_DIR = .ui
  MOC_DIR = .moc
  OBJECTS_DIR = .obj
}

FORMS	= mainform.ui \
	settingsdialog.ui
IMAGES	= images/filenew \
	images/fileopen \
	images/filesave \
	images/print \
	images/undo \
	images/redo \
	images/editcut \
	images/editcopy \
	images/editpaste \
	images/searchfind \
	images/1.xpm \
	images/2.xpm \
	images/3.xpm \
	images/4.xpm \
	images/arrowl.jpg \
	images/arrowr.jpg \
	images/video.jpg \
	images/crosshair.jpg \
	images/stop.jpeg
TEMPLATE	=app
CONFIG	+= qt warn_on release thread
INCLUDEPATH	+= ./video /usr/include/kde
LIBS	+= -lkdeui -lXv -ljpeg -lImlib /usr/local/lib/libxvidcore.a
LANGUAGE	= C++
