"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui
import matplotlib as mpl
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg\
    as MplToolbar
from matplotlib.backend_bases import cursors as mplCursors
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
import numpy

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs.resources import icons, cursors

#---------------------------------------------------------------------------
# Normal code begins
#--------------------------------------------------------------------------


mpl.rcdefaults()
mpl.rcParams['axes.formatter.limits'] = [-4, 4]
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['legend.fontsize'] = 'small'
MplToolbar.margin = 4

numpy.seterr(all='ignore')


class Toolbar(MplToolbar):

    def __init__(self, *args, **kwargs):
        pixmap = QtGui.QPixmap()
        pixmap.load(':/cross.png')
        mplCursors.SELECT_POINT = pixmap
        super(Toolbar, self).__init__(*args, **kwargs)

    def _init_toolbar(self):
        self.basedir = os.path.join(mpl.rcParams[ 'datapath' ],'images')

        a = self.addAction(self._icon('home.svg'), 'Home', self.home)
        a.setToolTip('Reset original view')
        a = self.addAction(self._icon('back.svg'), 'Back', self.back)
        a.setToolTip('Back to previous view')
        a = self.addAction(self._icon('forward.svg'), 'Forward', self.forward)
        a.setToolTip('Forward to next view')
        self.addSeparator()
        a = self.addAction(self._icon('move.svg'), 'Pan', self.pan)
        a.setToolTip('Pan axes with left mouse, zoom with right')
        a = self.addAction(self._icon('zoom_to_rect.svg'), 'Zoom', self.zoom)
        a.setToolTip('Zoom to rectangle')
        a = self.addAction(QtGui.QIcon(':/crosshairs.svg'), 'Select',
                           self.selectPointMode)
        a.setToolTip('Select the nearest data point')
        self.addSeparator()
        a = self.addAction(self._icon('subplots.png'), 'Subplots',
                self.configure_subplots)
        a.setToolTip('Configure subplots')
        a = self.addAction(self._icon('filesave.svg'), 'Save',
                self.save_figure)
        a.setToolTip('Save the figure')

        self.buttons = {}

        # Add the x,y location widget at the right side of the toolbar
        # The stretch factor is 1 which means any resizing of the toolbar
        # will resize this label instead of the buttons.
        if self.coordinates:
            self.locLabel = QtGui.QLabel( "", self )
            self.locLabel.setAlignment(
                    QtCore.Qt.AlignRight | QtCore.Qt.AlignTop )
            self.locLabel.setSizePolicy(
                QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                                  QtGui.QSizePolicy.Ignored))
            labelAction = self.addWidget(self.locLabel)
            labelAction.setVisible(True)

        # reference holder for subplots_adjust window
        self.adj_window = None

    def mouse_move(self, event):
        #print 'mouse_move', event.button

        if not event.inaxes or not self._active:
            if self._lastCursor != mplCursors.POINTER:
                self.set_cursor(mplCursors.POINTER)
                self._lastCursor = mplCursors.POINTER
        else:
            if self._active=='ZOOM':
                if self._lastCursor != mplCursors.SELECT_REGION:
                    self.set_cursor(mplCursors.SELECT_REGION)
                    self._lastCursor = mplCursors.SELECT_REGION
                if self._xypress:
                    x, y = event.x, event.y
                    lastx, lasty, a, ind, lim, trans = self._xypress[0]
                    self.draw_rubberband(event, x, y, lastx, lasty)
            elif (self._active=='PAN' and
                  self._lastCursor != mplCursors.MOVE):
                self.set_cursor(mplCursors.MOVE)

                self._lastCursor = mplCursors.MOVE
            elif self._active=='SELECT':
                if self._lastCursor != mplCursors.SELECT_POINT:
                    QtGui.QApplication.restoreOverrideCursor()
                    QtGui.QApplication.setOverrideCursor(
                                            QtGui.QCursor(mplCursors.SELECT_POINT))
                    self._lastCursor = mplCursors.SELECT_POINT

        if event.inaxes and event.inaxes.get_navigate():

            try: s = event.inaxes.format_coord(event.xdata, event.ydata)
            except ValueError: pass
            except OverflowError: pass
            else:
                if len(self.mode):
                    self.set_message('%s : %s' % (self.mode, s))
                else:
                    self.set_message(s)
        else: self.set_message(self.mode)

    def selectPointMode(self, *args):
        if self._active == 'SELECT':
            self._active = None
        else:
            self._active = 'SELECT'

        if self._idPress is not None:
            self._idPress = self.canvas.mpl_disconnect(self._idPress)
            self.mode = ''
        if self._idRelease is not None:
            self._idRelease = self.canvas.mpl_disconnect(self._idRelease)
            self.mode = ''

        if self._active:
            self._idRelease = self.canvas.mpl_connect(
                'button_release_event', self.selectPoint)
            self.mode = 'pixel select mode'
            self.canvas.widgetlock(self)
        else:
            self.canvas.widgetlock.release(self)

        self.set_message(self.mode)

    def selectPoint(self, event):
        if event.inaxes and event.inaxes.get_navigate():
            self.emit(QtCore.SIGNAL('pickEvent'), event.xdata, event.ydata)


class QtMplCanvas(FigureCanvasQTAgg):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None):
        self.figure = Figure()

        FigureCanvasQTAgg.__init__(self, self.figure)
        self.setParent(parent)

        FigureCanvasQTAgg.setSizePolicy(self,
                                        QtGui.QSizePolicy.Expanding,
                                        QtGui.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def _createInitialFigure(self, *args, **kwargs):
        raise NotImplementedError

    def enableAutoscale(self, *args, **kwargs):
        raise NotImplementedError

    def enableLogscale(self, *args, **kwargs):
        raise NotImplementedError

    def minimumSizeHint(self):
        return QtCore.QSize(0, 0)

    def sizeHint(self):
        w, h = self.get_width_height()
        return QtCore.QSize(w, h)

    def updateFigure(self, *args, **kwargs):
        raise NotImplementedError


class ElementCanvas(QtMplCanvas):

    _xlabel = ''
    _ylabel = ''
    _xlims = [0, 1]
    _ylims = [0, 1]

    def __init__(self, parent=None):
        QtMplCanvas.__init__(self, parent)
        self.axes = self.figure.add_subplot(111)

    def setXLabel(self, label):
        self._xlabel = label

    def setXLims(self, lims):
        self._xlims = lims

    def setYLabel(self, label):
        self._ylabel = label

    def setYLims(self, lims):
        self._ylims = lims


class ElementImage(ElementCanvas):

    autoscale = True

    def __init__(self, parent=None):
        ElementCanvas.__init__(self, parent)

        self._clim = [0, 1]
        self._image = None
        self._elementData = None
        self._colorbar = None

    def _createInitialFigure(self, elementData):
        self._elementData = elementData
        extent = []
        extent.extend(self._xlims)
        extent.extend(self._ylims)
        self._image = self.axes.imshow(elementData, extent=extent,
                                       aspect=1/1.414, interpolation='nearest',
                                       origin='lower')
        self._colorbar = self.figure.colorbar(self._image)

        self.axes.set_xlabel(self._xlabel)
        self.axes.set_ylabel(self._ylabel)

    def enableAutoscale(self, val):
        self.autoscale = val
        self.updateFigure()

    def setDataMax(self, val):
        self._clim[1] = val
        self.updateFigure()

    def setDataMin(self, val):
        self._clim[0] = val
        self.updateFigure()

    def setImageAspect(self, aspect):
        self.axes.set_aspect(1/aspect)
        self.updateFigure()

    def setInterpolation(self, val):
        self._image.set_interpolation('%s'%val)
        self.draw()

    def setImageOrigin(self, val):
        self._image.origin = '%s'%val
        self.draw()

    def updateFigure(self, elementData=None):
        if self._image is None:
            self._createInitialFigure(elementData)
        else:
            if elementData is None: elementData = self._elementData
            else: self._elementData = elementData
            self._image.set_data(elementData)

        if self.autoscale:
            self._image.autoscale()
            self._clim = list(self._image.get_clim())
            self.emit(QtCore.SIGNAL("dataMin(PyQt_PyObject)"), self._clim[0])
            self.emit(QtCore.SIGNAL("dataMax(PyQt_PyObject)"), self._clim[1])
        else:
            self._image.set_clim(self._clim)
        self.draw()


class ElementPlot(ElementCanvas):

    def __init__(self,parent=None):
        ElementCanvas.__init__(self, parent)

        self._elementData = None
        self._autoscale = True

    def _createInitialFigure(self, elementData):
        self._elementData = elementData

        self._elementPlot, = self.axes.plot(elementData, 'b')
        self.axes.set_xlabel(self._xlabel)
        self.axes.set_ylabel(self._ylabel)

    def enableAutoscale(self, val):
        self.axes.enable_autoscale_on(val)
        self.updateFigure()

    def setDataMax(self, val):
        self._ylims[1]=val
        self.updateFigure()

    def setDataMin(self, val):
        self._ylims[0]=val
        self.updateFigure()

    def updateFigure(self, elementData=None):
        if self._elementData is None:
            self._createInitialFigure(elementData)
        else:
            if elementData is None: elementData = self._elementData
            else: self._elementData = elementData

            self._elementPlot.set_ydata(elementData)
            self.axes.relim()
            self.axes.autoscale_view()

        self._elementData = elementData

        if self.axes.get_autoscale_on():
            self._ylims = list(self.axes.get_ylim())
            self.emit(QtCore.SIGNAL("dataMin(PyQt_PyObject)"), self._ylims[0])
            self.emit(QtCore.SIGNAL("dataMax(PyQt_PyObject)"), self._ylims[1])
        else:
            self.axes.set_ylim(self._ylims)

        self.draw()
