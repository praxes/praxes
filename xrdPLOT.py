from PyQt4.QtCore import *
from PyQt4.QtGui import *
from XRDdefaults import *
from xrd_fileIO_fcns import *
import numpy
import ui_mainmenu
import ui_message_box
import ui_import_image
import ui_import_attr
import ui_get_group
import sys
import os
import time
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

#import matplotlib.numerix.npyma as ma
import numpy.ma as ma
import matplotlib.colors as colors
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import pylab

class plotwidget(FigureCanvas):
    def __init__(self, parent, width=5, height=5, dpi=100, showcolbar=True, nav=True):
        #super(plotwidget, self).__init__(parent) #***
        #plotdata can be 2d array for image plot or list of 2 1d arrays for x-y plot or 2d array for image plot or list of lists of 2 1D arrays
        self.marwidth=3450
        self.colbar=None
        self.showcolbar=showcolbar
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111, navigate=nav)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.parent=parent
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.mpl_connect('button_press_event', self.myclick)
#        self.widthpix=width*dpi
#        self.heightpix=height*dpi
        self.clickcount=1
        self.clickptlist=[]

    def gettoolbarinstance(self):
        NavigationToolbar(self, self.parent)

    def reinit(self):
        self.axes.cla()
        self.im=None
        self.fig.canvas.draw()

    def performplot(self, plotdata, overlay=False, log=False, ylowlimit=None, upperorigin=True, axesformat='mar', qvals=None, chivals=None,  peaklist=None, formstr='', alsoprint=False, colrange=None, cmap=matplotlib.cm.jet, aspect=None, extent=None):
    #peak list is a list of x and list of y where green peak dots will be placed - plotdata must be a list of 1d data for this
        self.axes.hold(overlay)
        if isinstance(plotdata, numpy.ndarray) and len(plotdata.shape)==2:
            if upperorigin:
                originstr='upper'
            else:
                originstr='lower'
            if log:
                if (plotdata<0).sum()==0:
                    if (plotdata==0).sum():
                        plotdata[plotdata>0.]=numpy.log10(plotdata[plotdata>0.])

            if aspect is None:
                aspect=plotdata.shape[1]/(1.0*plotdata.shape[0])
            if colrange is None:
                colrange=(plotdata.min(),plotdata.max())
            if self.colbar is None or self.im is None:
                self.im=self.axes.imshow(plotdata, origin=originstr, aspect=aspect, cmap=cmap, interpolation='nearest', vmin=colrange[0], vmax=colrange[1])
            else:
                self.im.set_data(plotdata)
                self.im.set_clim(colrange[0], colrange[1])
                self.im.axes.set_xlim([-.5, plotdata.shape[1]+0.5])
                yl=[-.5, plotdata.shape[0]+0.5]
                if upperorigin:
                    yl.reverse()
                self.im.axes.set_ylim(yl)
                self.im.axes.set_aspect(aspect)
                self.im.changed()

            if self.showcolbar and self.colbar is None:
                    self.colbar=self.fig.colorbar(self.im)
            if not extent is None:
                self.im.set_extent(extent)
            if axesformat=='mar':
                self.marimageaxesformat(plotdata.shape[0])
            if axesformat=='qq':
                self.qqimageaxesformat(qvals)
            if axesformat=='chiq':
                self.chiqimageaxesformat(chivals, qvals)


        elif isinstance(plotdata, list) and isinstance(plotdata[0], numpy.ndarray) and len(plotdata)==2:
            if len(formstr)>0:
                self.axes.plot(plotdata[0], plotdata[1], formstr)
                if alsoprint:
                    print 'print while plotting: ', time.ctime()
                    print numpy.array([plotdata[0], plotdata[1]]).T

            else:
                self.axes.plot(plotdata[0], plotdata[1])
                if alsoprint:
                    print 'print while plotting: ', time.ctime()
                    print numpy.array([plotdata[0], plotdata[1]]).T
            if not peaklist is None:
                self.axes.hold(True)
                self.axes.plot(peaklist[0], peaklist[1], 'g.')
                if alsoprint:
                    print 'print peaklist while plotting: ', time.ctime()
                    print numpy.array([peaklist[0], peaklist[1]]).T
                self.axes.hold(overlay)
            if log:
                self.axes.set_yscale('log')
            else:
                self.axes.set_yscale('linear')
        elif isinstance(plotdata, list) and isinstance(plotdata[0], list) and isinstance(plotdata[0, 0], numpy.ndarray):
            c=sum(plotdata,[])
            for i in range(len(c)):
                d=''.join((d,'c[','%d' %i,'],'))
            self.axes.plot(eval(d[0:-1]))
            if log:
                self.axes.set_yscale('log')
            else:
                self.axes.set_yscale('linear')
        else:
            QMessageBox.warning(self.parent,"plot type error",  "Plot failed because did not recognize datatype")
        if ylowlimit is not None:
            self.axes.set_ylim(ylowlimit, self.axes.get_ylim()[1])
        self.fig.canvas.draw()

    def performqqnormpeakplot(self, plotdata, overlay=False, ylowlimit=None, upperorigin=False, axesformat='qq', qvals=None, cmap=matplotlib.cm.autumn, aspect=None, colrange=None):
        self.axes.hold(overlay)

        if upperorigin:
            originstr='upper'
        else:
            originstr='lower'

        if aspect is None:
            aspect=plotdata.shape[1]/(1.0*plotdata.shape[0])
        if colrange is None:
            colrange=(plotdata.min(),plotdata.max())
        if self.colbar is None or self.im is None:
            self.im=self.axes.imshow(plotdata, origin=originstr, aspect=aspect, cmap=cmap, interpolation='nearest', vmin=colrange[0], vmax=colrange[1])
        else:
            self.im.set_data(plotdata)
            self.im.set_clim(colrange[0], colrange[1])
            self.im.changed()

        if self.showcolbar and self.colbar is None:
            self.colbar=self.fig.colorbar(self.im)


        if axesformat=='mar':
            self.marimageaxesformat(plotdata.shape[0])
        if axesformat=='qq':
            self.qqimageaxesformat(qvals)

        if ylowlimit is not None:
            self.axes.set_ylim(ylowlimit, self.axes.get_ylim()[1])

    def performqqtreeplot(self, plotdata, redindarr, blueind2darr,  qvals, upperorigin=False, cmap=matplotlib.cm.Greys, aspect=None, colrange=None):
        self.axes.hold(False)

        if upperorigin:
            originstr='upper'
        else:
            originstr='lower'

        if aspect is None:
            aspect=plotdata.shape[1]/(1.0*plotdata.shape[0])
        if colrange is None:
            colrange=(plotdata.min(),plotdata.max())
        if self.colbar is None or self.im is None:
            self.im=self.axes.imshow(plotdata, origin=originstr, aspect=aspect, cmap=cmap, interpolation='nearest', vmin=colrange[0], vmax=colrange[1])
        else:
            self.im.set_data(plotdata)
            self.im.set_clim(colrange[0], colrange[1])
            self.im.changed()

        if self.showcolbar and self.colbar is None:
            self.colbar=self.fig.colorbar(self.im)
        self.axes.hold(True)

        if not redindarr is None:
            for ind in redindarr:
                self.axes.plot([ind, ind, len(qvals)-1], [0, ind, ind], 'r')
        if not blueind2darr is None:
            for indpair in blueind2darr:
                self.axes.plot([max(indpair)], [min(indpair)], 'b.')

        if not qvals is None:
            self.axes.set_xlim(0, len(qvals))
            self.axes.set_ylim(0, len(qvals))
            self.qqimageaxesformat(qvals)

    def save(self, name):
        self.fig.savefig(''.join((name, '.png')), dpi=300)

    def sizeHint(self):
        w, h = self.get_width_height()
        return QSize(w, h)

    def minimumSizeHint(self):
        return QSize(10, 10)

    def myclick(self, event):
        if not (event.xdata is None or event.ydata is None):
            arrayxy=[event.ydata, event.xdata]
            print 'clicked on image: array indeces ', arrayxy
            self.emit(SIGNAL("genericclickonplot"), [event.xdata, event.ydata])
            if self.clickcount<0:
                self.clickptlist+=[arrayxy]

            self.clickcount+=1

            if self.clickcount==0:
                self.clickcount=1
                self.emit(SIGNAL("clicksdone"), self.clickptlist)

    def countclicks(self, numclicks):
        self.clickcount=-1*numclicks
        self.clickptlist=[]

    def marimageaxesformat(self, width):  #this somehow screws up the image so skip it until figure out what is going on
        return
        bin=self.marwidth/(1.0*width)
        interval=1000
        binint=1000//bin
        ticks=[]
        ticknames=[]
        for i in range(numpy.uint16(width//binint+1)):
            ticks+=[i*binint]
            ticknames+=['%d' %(i*interval)]
        self.axes.set_xticklabels(ticknames, fontsize=6)
        self.axes.set_yticklabels(ticknames,fontsize=6)
        self.axes.set_xticks(ticks)
        self.axes.set_yticks(ticks)


    def qqimageaxesformat(self, qvals):
        return
        pix=len(qvals)
        ticks=[0, pix//5, 2*pix//5, 3*pix//5, 4*pix//5, pix-1]
        ticknames=[]
        for i in ticks:
            ticknames+=['%d' %(qvals[i])]
        self.axes.set_xticklabels(ticknames, fontsize=6)
        self.axes.set_yticklabels(ticknames,fontsize=6)
        self.axes.set_xticks(ticks)
        self.axes.set_yticks(ticks)

    def chiqimageaxesformat(self, chivals, qvals):
        return
        pix=len(qvals)
        ticks=[0, pix//5, 2*pix//5, 3*pix//5, 4*pix//5, pix-1]
        ticknames=[]
        for i in ticks:
            ticknames+=['%d' %(qvals[i])]

        chipix=len(chivals)
        chiticks=[0, chipix//5, 2*chipix//5, 3*chipix//5, 4*chipix//5, chipix-1]
        chiticknames=[]
        for i in chiticks:
            chiticknames+=['%d' %(chivals[i])]

        self.axes.set_xticklabels(chiticknames, fontsize=6)
        self.axes.set_yticklabels(ticknames,fontsize=6)
        self.axes.set_xticks(chiticks)
        self.axes.set_yticks(ticks)

class subnavigatorwidget(FigureCanvas):
    def __init__(self, parent, xgrid, zgrid, xcoords, zcoords, width=3, dpi=100):
        self.xgrid=xgrid
        self.zgrid=zgrid
        self.xcoords=xcoords
        self.zcoords=zcoords
        self.widthpix=width*dpi
        self.substrateradius=38.1
        self.subfactor=numpy.sqrt(self.substrateradius/38.1) #the axes scales are not automated,

        self.fig = Figure(figsize=(width, width), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.axes = self.fig.add_subplot(111, aspect=1, frame_on=False)
        temp=self.axes.get_position().get_points()
        self.radiusmm=self.substrateradius+4
        self.pixpermm=temp[1, 0]*self.widthpix/(2.0*self.radiusmm)
        self.xpixshift=(temp[0, 0]+temp[1, 0]/2.0)*self.widthpix
        self.ypixshift=(temp[0, 1]+temp[1, 0]/2.0)*self.widthpix
        #self.axes.set_axis_bgcolor('w') #this doesn't seem to work
        self.axesformat()
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        self.mpl_connect('button_press_event', self.myclick)

        self.inxvals=[]
        self.inzvals=[]
        self.exxvals=[]
        self.exzvals=[]
        self.includelist=[]
        self.excludelist=[]

        FigureCanvas.setSizePolicy(self, QSizePolicy.Fixed, QSizePolicy.Fixed)
        FigureCanvas.updateGeometry(self)

    def reinit(self, xgrid=None, zgrid=None, xcoords=None, zcoords=None, includelist=None,  excludelist=None):
        if not self.xgrid is None:
            self.xgrid=xgrid
        if not self.zgrid is None:
            self.zgrid=zgrid
        if not xcoords is None:
            self.xcoords=xcoords
        if not zcoords is None:
            self.zcoords=zcoords
        if not includelist is None:
            self.includelist=includelist
            self.inxvals,  self.inzvals = self.getxzcoords(self.includelist)
        if not excludelist is None:
            self.excludelist=excludelist
            self.exxvals, self.exzvals = self.getxzcoords(self.excludelist)

        self.xsel, self.zsel = (None, None)

        self.axes.cla()
        self.axes.hold(False)
        self.axesformat()
        self.performplot()

    def plotpoints(self, includelist,  excludelist, select=None):
        self.includelist=includelist
        self.excludelist=excludelist
        temparr=numpy.float32([self.xgrid[1], self.zgrid[1]])
        self.clickradiusmm=numpy.min(temparr[temparr!=0.])/2.0
        if min(self.xgrid[1], self.zgrid[1])*self.pixpermm>7:
            self.inmark='g.'
            self.outmark='m.'
        else:
            self.inmark='g,'
            self.outmark='m,'

        self.inxvals,  self.inzvals = (self.xcoords[numpy.int16(self.includelist)], self.zcoords[numpy.int16(self.includelist)])
        self.exxvals, self.exzvals = (self.xcoords[numpy.int16(self.excludelist)], self.zcoords[numpy.int16(self.excludelist)])
        if select is not None:
            self.xsel, self.zsel =(self.xcoords[numpy.int16(select)], self.zcoords[numpy.int16(select)])
        else:
            self.xsel, self.zsel = (None, None)
        self.performplot()

    def myclick(self, event):
#        xmm=(event.x-self.xpixshift)/self.pixpermm
#        zmm=(self.ypixshift-event.y)/self.pixpermm
        if not ((event.xdata is None) or (event.ydata is None)):
            picnum = self.clickchecker(event.xdata, event.ydata)
            if picnum is not None:
                self.emit(SIGNAL("picclicked"), picnum)

    def clickchecker(self, xmm, zmm):
        for i in range(len(self.includelist)):
            if (self.inxvals[i]-xmm)**2+(self.inzvals[i]+zmm)**2<self.clickradiusmm**2: #the z distance calculation uses + because -z is plotted
                return self.includelist[i]
        for i in range(len(self.excludelist)):
            if (self.exxvals[i]-xmm)**2+(self.exzvals[i]+zmm)**2<self.clickradiusmm**2:
                return self.excludelist[i]
        return None

    def performplot(self):

        self.circleplot()

        if len(self.inxvals)>0:
            self.axes.plot(self.inxvals, [-1.*i for i in self.inzvals], self.inmark, linestyle='None')

        if len(self.exxvals)>0:
            self.axes.plot(self.exxvals,  [-1.*i for i in self.exzvals], self.outmark, linestyle='None')

        if self.xsel is not None:
            self.axes.plot(self.xsel, [-1.*i for i in self.zsel], 'bo', linestyle='None')

        self.axesformat()


    def save(self, name):
        self.fig.savefig(''.join((name, '.png')))

    def sizeHint(self):
        return QSize(self.widthpix, self.widthpix)

    def axesformat(self):
        self.axes.set_xlim(-1*self.radiusmm, self.radiusmm)
        self.axes.set_ylim(-1*self.radiusmm, self.radiusmm)
        self.axes.set_xticklabels(['-40', '-30', '-20', '-10', '0', '10', '20', '30', '40'], fontsize=8)
        self.axes.set_yticklabels(['40', '30', '20', '10', '0', '-10', '-20', '-30', '-40'],fontsize=8)
        self.axes.set_xticks([-40, -30, -20, -10, 0, 10, 20, 30, 40])
        self.axes.set_yticks([-40, -30, -20, -10, 0, 10, 20, 30, 40])
        self.axes.hold(False)

    def plotneighbors(self, neighbors):
        self.axes.hold(True)
        for ind1, neighlist in enumerate(neighbors):
            for ind2 in neighlist:
                if ind1 in self.includelist and ind2 in self.includelist:
                    localind1=numpy.where(self.includelist==ind1)[0]
                    localind2=numpy.where(self.includelist==ind2)[0]
                    self.axes.plot([self.inxvals[localind1], self.inxvals[localind2]],  [-1.*self.inzvals[localind1], -1.*self.inzvals[localind2]], color='red',lw=.5)

    def circleplot(self):

        xcirc= self.subfactor*numpy.array([36.1 ,  36.02,  35.81,  35.46,  34.96,  34.33,  33.56,  32.66, \
 31.63,  30.48,  29.2 ,  27.81,  26.31,  24.71,  23.01,  21.21, \
 19.34,  17.39,  15.37,  13.28,  11.15,   8.97,   6.76,   4.52, \
  2.26,   0.  ,  -2.26,  -4.52,  -6.76,  -8.97, -11.15, -13.28, \
-15.37, -17.39, -19.34, -21.21, -23.01, -24.71, -26.31, -27.81, \
-29.2 , -30.48, -31.63, -32.66, -33.56, -34.33, -34.96, -35.46, \
-35.81, -36.02, -36.1 , -36.02, -35.81, -35.46, -34.96, -34.33, \
-33.56, -32.66, -31.63, -30.48, -29.2 , -27.81, -26.31, -24.71, \
-23.01, -21.21, -19.34, -17.39, -15.37, -13.28, -11.15,  -8.97, \
 -6.76,  -4.52,  -2.26,   0.  ,   2.26,   4.52,   6.76,   8.97, \
 11.15,  13.28,  15.37,  17.39,  19.34,  21.21,  23.01,  24.71, \
 26.31,  27.81,  29.2 ,  30.48,  31.63,  32.66,  33.56,  34.33, \
 34.96,  35.46,  35.81,  36.02,  36.1 ])

        ycirc= self.subfactor*numpy.array([0.  ,   2.26,   4.52,   6.76,   8.97,  11.15,  13.28,  15.37,\
 17.39,  19.34,  21.21,  23.01,  24.71,  26.31,  27.81,  29.2 ,\
 30.48,  31.63,  32.66,  33.56,  34.33,  34.96,  35.46,  35.81,\
 36.02,  36.1 ,  36.02,  35.81,  35.46,  34.96,  34.33,  33.56,\
 32.66,  31.63,  30.48,  29.2 ,  27.81,  26.31,  24.71,  23.01,\
 21.21,  19.34,  17.39,  15.37,  13.28,  11.15,   8.97,   6.76,\
  4.52,   2.26,   0.  ,  -2.26,  -4.52,  -6.76,  -8.97, -11.15,\
-13.28, -15.37, -17.39, -19.34, -21.21, -23.01, -24.71, -26.31,\
-27.81, -29.2 , -30.48, -31.63, -32.66, -33.56, -34.33, -34.96,\
-35.46, -35.81, -36.02, -36.1 , -36.02, -35.81, -35.46, -34.96,\
-34.33, -33.56, -32.66, -31.63, -30.48, -29.2 , -27.81, -26.31,\
-24.71, -23.01, -21.21, -19.34, -17.39, -15.37, -13.28, -11.15,\
 -8.97,  -6.76,  -4.52,  -2.26,   0.  ])

        self.axes.plot(xcirc, ycirc, 'k-')
        self.axes.hold(True)

class compnavigatorwidget(FigureCanvas):
    def __init__(self, parent, comp, elstrlist, width=3, dpi=100):
        self.comp=comp
        self.cart=cart_comp(comp)

        compdist=compdistarr_comp(self.comp)
        mincompdist=numpy.min(compdist[compdist>0.])
        self.clickradius=max(.02, mincompdist/2.0)
        self.elstrlist=elstrlist

        self.widthpix=width*dpi
        self.fig = Figure(figsize=(width/.866, width), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.axes = self.fig.add_subplot(111, aspect=.866, frame_on=False)

        self.pixpercomp=self.widthpix

        #self.axes.set_axis_bgcolor('w') #this doesn't seem to work
        self.axesformat()
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        self.mpl_connect('button_press_event', self.myclick)

        self.inxvals=[]
        self.inzvals=[]
        self.exxvals=[]
        self.exzvals=[]
        self.includelist=[]
        self.excludelist=[]

        FigureCanvas.setSizePolicy(self, QSizePolicy.Fixed, QSizePolicy.Fixed)
        FigureCanvas.updateGeometry(self)

    def reinit(self, comp=None, elstrlist=None, includelist=None,  excludelist=None):
        if not comp is None:
            self.comp=comp
            self.cart=cart_comp(comp)

            compdist=compdistarr_comp(self.comp)
            mincompdist=numpy.min(compdist[compdist>0.])
            self.clickradius=max(.02, mincompdist/2.0)
        if not elstrlist is None:
            self.elstrlist=elstrlist
        if not includelist is None:
            self.includelist=includelist
        self.inxvals,  self.inzvals = self.getxzcoords(self.includelist)
        if not excludelist is None:
            self.excludelist=excludelist
        self.exxvals, self.exzvals = self.getxzcoords(self.excludelist)

        self.xsel, self.zsel = (None, None)

        self.axes.hold(False)
        self.axes.cla()
        self.axesformat()
        self.performplot()

    def getxzcoords(self, inds):
        inds=numpy.int16(inds)
        x=self.cart[inds, 0]
        z=self.cart[inds, 1]
        return x, z

    def plotpoints(self, includelist,  excludelist, select=None):
        self.includelist=includelist
        self.excludelist=excludelist

        #if self.clickradius>?:
        if True:
            self.inmark='g.'
            self.outmark='m.'
        else:
            self.inmark='g,'
            self.outmark='m,'

        self.inxvals,  self.inzvals = self.getxzcoords(self.includelist)
        self.exxvals, self.exzvals = self.getxzcoords(self.excludelist)
        if select is not None:
            self.xsel, self.zsel = self.getxzcoords(select)
        else:
            self.xsel, self.zsel = (None, None)
        self.performplot()

    def myclick(self, event):
        if not ((event.xdata is None) or (event.ydata is None)):
            picnum = self.clickchecker(event.xdata, event.ydata)
            if picnum is not None:
                self.emit(SIGNAL("picclicked"), picnum)

    def clickchecker(self, x, z):
        ind=numpy.array([(xi-x)**2+(zi-z)**2 for xi, zi in zip(self.inxvals, self.inzvals)])
        exd=numpy.array([(xi-x)**2+(zi-z)**2 for xi, zi in zip(self.exxvals, self.exzvals)])
        if len(ind)>0 and ind.min()<self.clickradius**2 and (len(exd)==0 or ind.min()<exd.min()):
            return self.includelist[myargmin(ind)]
        elif len(exd)>0 and exd.min()<self.clickradius**2:
            return self.excludelist[myargmin(exd)]
        return None

    def performplot(self):

        self.triangleplot()

        if len(self.inxvals)>0:
            self.axes.plot(self.inxvals, self.inzvals, self.inmark, linestyle='None')

        if len(self.exxvals)>0:
            self.axes.plot(self.exxvals,  self.exzvals, self.outmark, linestyle='None')

        if self.xsel is not None:
            self.axes.plot(self.xsel, self.zsel, 'bo', linestyle='None')

        self.axesformat()


    def save(self, name):
        self.fig.savefig(''.join((name, '.png')))

    def sizeHint(self):
        return QSize(self.widthpix, self.widthpix)

    def axesformat(self):
        self.axes.set_xlim(0., 1.)
        self.axes.set_ylim(0., 1.)
        self.axes.set_xticklabels(['0.2', '0.4', '0.6', '0.8'], fontsize=8)
        self.axes.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1'],fontsize=8)
        self.axes.set_xticks([.2, .4, .6, .8])
        self.axes.set_yticks([.2, .4, .6, .8, 1.])
        for count, el in enumerate(self.elstrlist):
            if el=='' or el=='X':
                continue
            if count==0:
                self.axes.text(0., 0., el,fontsize=10,ha='right',va='top')
            elif count==1:
                self.axes.text(.5, 1., el,fontsize=10,ha='center',va='bottom')
            elif count==2:
                self.axes.text(1., 0., el,fontsize=10,ha='left',va='top')
        self.axes.hold(False)

    def plotneighbors(self, neighbors):
        self.axes.hold(True)
        for ind1, neighlist in enumerate(neighbors):
            for ind2 in neighlist:
                if ind1 in self.includelist and ind2 in self.includelist:
                    localind1=numpy.where(self.includelist==ind1)[0]
                    localind2=numpy.where(self.includelist==ind2)[0]
                    self.axes.plot([self.inxvals[localind1], self.inxvals[localind2]],  [self.inzvals[localind1], self.inzvals[localind2]], color='red',lw=.5)

    def triangleplot(self):
        xtri= numpy.array([0., .5, 1., 0.])
        ytri= numpy.array([0., 1., 0., 0.])

        self.axes.plot(xtri, ytri, 'k-')
        self.axes.hold(True)

class wavelet1dplotwidget(FigureCanvas):
    def __init__(self, parent, qgrid, qscalegrid, qposngrid, width=10, height=8, dpi=100, showcolbar=True):
        #super(plotwidget, self).__init__(parent) #***
        #plotdata can be 2d array for image plot or list of 2 1d arrays for x-y plot or 2d array for image plot or list of lists of 2 1D arrays
        self.colbar=None
        self.showcolbar=showcolbar
        self.fig=Figure(figsize=(width, height), dpi=dpi)
        axes=self.fig.add_subplot(211)
        axes.hold(False)
        axes=self.fig.add_subplot(212)
        axes.hold(False)

        self.qgrid=qgrid
        self.qscalegrid=qscalegrid
        self.qposngrid=qposngrid

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.parent=parent
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
#        self.widthpix=width*dpi
#        self.heightpix=height*dpi

        self.wtaxes=self.fig.add_subplot(212)
        self.qlim=(-.5, self.qposngrid[2]-1+.5)
        minq=int(round(q_qgrid_ind(self.qposngrid, 0)))
        maxq=int(round(q_qgrid_ind(self.qposngrid, self.qposngrid[2]-1)))
        qlabelvals=numpy.uint16(range(minq, maxq, max(1, (maxq-minq)//9))[:-1]+[maxq])
        self.qlabels=['%d' %q for q in qlabelvals]
        self.qlabelposnind=ind_qgrid_q(self.qposngrid, numpy.float32(qlabelvals), fractional=True)
        self.wtaxes.set_xticks(self.qlabelposnind)
        self.wtaxes.set_xticklabels(self.qlabels)

        self.scalelim=(-.5, self.qscalegrid[2]-1+.5)
        qslabelind=numpy.float32(range(5))*(self.qscalegrid[2]-1.0)/4.0
        qslabels=['%.1f' %qs for qs in scale_scalegrid_ind(self.qscalegrid, qslabelind)]

        self.wtaxes.set_yticks(qslabelind)
        self.wtaxes.set_yticklabels(qslabels)

        self.dataaxes=self.fig.add_subplot(211, sharex=self.wtaxes)
        self.dataaxes.set_yticks([])
        self.dataaxes.set_yticks([])
        self.fig.subplots_adjust(right=0.85)

        self.mpl_connect('button_press_event', self.myclick)
    def myclick(self, event):
        if not ((event.xdata is None) or (event.ydata is None)):
            if event.inaxes==self.dataaxes:
                self.emit(SIGNAL("dataaxesclicked"), [event.xdata, event.ydata])
            if event.inaxes==self.wtaxes:
                self.emit(SIGNAL("wtaxesclicked"), [event.xdata, event.ydata])

    def display_wavetrans1d(self, wt, ridges, data, datascaleind, datapeakind=None, wtcmap=cm.jet, ridgecmap=cm.gray, motherchildline_clrwidth=('k-', 1.5),  title='', logdata=False):
        self.dataaxes.set_yticks([])
        self.dataaxes.set_yticks([])
        ridgewtscatter=[]
        for r in ridges:
            scaleinds=numpy.where((r!=32767)&(r>=0))
            posninds=r[scaleinds]
            scaleinds_increasingscale=wt.shape[0]-scaleinds[0]-1
            motherind=motherridgeind_childridge(r)
            if motherind is None:
                mothertochildplotcoords=None
            else:
                print 'MOTHERIND', motherind
                print r
                print len(ridgewtscatter), len(ridgewtscatter[motherind])
                print len(ridgewtscatter[motherind][0]), len(ridgewtscatter[motherind][1])
                xmother=ridgewtscatter[motherind][0][-1]
                ymother=ridgewtscatter[motherind][1][-1]
                xchild=posninds[0]
                ychild=scaleinds_increasingscale[0]
                mothertochildplotcoords=([xmother, xchild], [ymother, ychild])#assume that mother ridges always appear in "ridges" before the children ridges
            ridgewtscatter+=[(posninds, scaleinds_increasingscale, wt[(scaleinds_increasingscale, posninds)], mothertochildplotcoords)]
        if datascaleind is None:
            qpind_data=ind_qgrid_q(self.qposngrid, q_qgrid_ind(self.qgrid), fractional=True)
            colstr='b'
        else:
            qpind_data=numpy.array(range(int(round(self.qposngrid[2]))))
            colstr='g'

        aspect=.3*self.qposngrid[2]/self.qscalegrid[2]
        #vmin, vmax=numpy.min(wt[numpy.logicalnotnumpy.isnan(wt)

        maskedwt = ma.masked_where(numpy.isnan(wt), numpy.sign(wt)*numpy.sqrt(numpy.abs(wt)))


        self.wtaxes.clear()

        if self.colbar is None or self.im is None:
            self.im=self.wtaxes.imshow(maskedwt, origin='lower', aspect=aspect, cmap=wtcmap, interpolation='nearest')
        else:
            actuallyshownim=self.wtaxes.imshow(maskedwt, origin='lower', aspect=aspect, cmap=wtcmap, interpolation='nearest')
            self.im.set_data(maskedwt)
            self.im.set_clim(maskedwt.min(), maskedwt.max())
            self.im.set_cmap(wtcmap)
            self.colbar.set_cmap(wtcmap)
            self.im.changed()

        if self.colbar is None:
            self.colbaraxes=self.fig.add_axes([0.9, 0.1, 0.02, 0.3])
            self.colbar=self.fig.colorbar(self.im, cmap=wtcmap, cax=self.colbaraxes)

        self.wtaxes.set_xticks(self.qlabelposnind)
        self.wtaxes.set_xticklabels(self.qlabels)
        self.wtaxes.set_xlabel('wavelet q-position (1/nm)')
        self.wtaxes.set_ylabel('wavelet q-scale (1/nm)')
        self.wtaxes.hold(True)

        for x, y, c, motherchild in ridgewtscatter:
            if ridgecmap is None:
                self.wtaxes.plot(x, y, 'o')
            else:
                self.wtaxes.scatter(x, y, c=c, cmap=ridgecmap)
            if not (motherchild is None) and not (motherchildline_clrwidth is None):
                self.wtaxes.plot(motherchild[0], motherchild[1], motherchildline_clrwidth[0], linewidth=motherchildline_clrwidth[1])

        self.dataaxes.clear()
        self.dataaxes.hold(False)

        datainds=numpy.where(numpy.logical_not(numpy.isnan(data)))
        self.dataaxes.plot(qpind_data[datainds], data[datainds], colstr, linewidth=3)
        self.dataaxes.hold(True)

        if not (datapeakind is None):
            if datascaleind is None:
                for x, y in zip(ind_qgrid_q(self.qposngrid, q_qgrid_ind(self.qgrid, datapeakind), fractional=True), data[(numpy.uint16(numpy.round(datapeakind)), )]):
                    self.dataaxes.plot([x, x], [data[numpy.logical_not(numpy.isnan(data))].min(), y], 'r')
            else:
                self.dataaxes.plot(datapeakind, data[(numpy.uint16(numpy.round(datapeakind)), )], 'k*',  markersize=11)

        if logdata:
            self.dataaxes.set_yscale('log')
        else:
            self.dataaxes.set_yscale('linear')

        self.dataaxes.hold(False)
        if datascaleind is None:
            self.dataaxes.set_xlabel('scattering vector (1/nm)')
            self.dataaxes.set_ylabel('diffraction intensity')
        else:
            self.dataaxes.set_xlabel('wavelet q-position (1/nm)')
            self.dataaxes.set_ylabel('wavelet transform at q-scale %.2f /nm' %scale_scalegrid_ind(self.qscalegrid, datascaleind))

        qslabelind=numpy.float32(range(5))*(self.qscalegrid[2]-1.0)/4.0
        qslabels=['%.1f' %qs for qs in scale_scalegrid_ind(self.qscalegrid, qslabelind)]

        self.wtaxes.set_yticks(qslabelind)
        self.wtaxes.set_yticklabels(qslabels)

        self.dataaxes.set_xlim(self.qlim)
        self.wtaxes.set_xlim(self.qlim)
        self.wtaxes.set_ylim(self.scalelim)




    def plot1doverlay(self, data, datascaleind, datapeakind=None):
        self.dataaxes.hold(True)
        if datascaleind is None:
            qpind_data=ind_qgrid_q(self.qposngrid, q_qgrid_ind(self.qgrid), fractional=True)
            colstr='b'
        else:
            qpind_data=numpy.array(range(int(round(self.qposngrid[2]))))
            colstr='g'

        self.dataaxes.plot(qpind_data, data, colstr)

        if not (datapeakind is None):
            if datascaleind is None:
                for x, y in zip(ind_qgrid_q(self.qposngrid, q_qgrid_ind(self.qgrid, datapeakind), fractional=True), data[(numpy.uint16(numpy.round(datapeakind)), )]):
                    self.dataaxes.plot([x, x], [data.min(), y], 'r')
            else:
                self.dataaxes.plot(datapeakind, data[(numpy.uint16(numpy.round(datapeakind)), )], 'k+')

        if datascaleind is None:
            self.dataaxes.set_xlabel('scattering vector (1/nm)')
            if 'wavelet' in self.dataaxes.get_ylabel():
                self.dataaxes.set_ylabel('wavelet, diffraction intensity')
        else:
            if 'wavelet' in self.dataaxes.get_ylabel():
                self.dataaxes.set_ylabel(self.dataaxes.get_ylabel() +', %.2f /nm' %scale_scalegrid_ind(self.qscalegrid, datascaleind))
            else:
                self.dataaxes.set_ylabel('wavelet, diffraction intensity')

    def save(self, name):
        self.fig.savefig(''.join((name, '.png')), dpi=300)


class interpimage1dplotwidget(FigureCanvas):
    def __init__(self, parent, qgrid, qscalegrid, qposngrid, width=12, height=6, dpi=100, showcolbar=True):
        #super(plotwidget, self).__init__(parent) #***
        #plotdata can be 2d array for image plot or list of 2 1d arrays for x-y plot or 2d array for image plot or list of lists of 2 1D arrays
        self.colbar=None
        self.showcolbar=showcolbar
        self.fig=Figure(figsize=(width, height), dpi=dpi)
        self.axes=self.fig.add_subplot()
        axes.hold(True)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.parent=parent
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
#        self.widthpix=width*dpi
#        self.heightpix=height*dpi
    def save(self, name):
        self.fig.savefig(''.join((name, '.png')), dpi=300)
