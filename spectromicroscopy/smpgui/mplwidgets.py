"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg, \
    NavigationToolbar2QTAgg
from matplotlib.figure import Figure

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Normal code begins
#--------------------------------------------------------------------------

class MplCanvas(FigureCanvasQTAgg):
    """This is a QWidget as well as a FigureCanvasAgg"""
    def __init__(self, visual, matrix, x, y, vmin, vmax,parent=None,
                 energy_matrix=None, plot_matrix=None, scale="linear",
                 width=5, height=4, dpi=100):
        self.plot_matrix = plot_matrix
        self.energy_matrix = energy_matrix
        self.scale = scale
        self.visual = visual
        self.x = x
        self.y = y
        self.min = vmin
        if vmax == 0:
            self.max = None
            self.min = None
        elif vmin > vmax:
            self.min = vmax
            self.max = vmin
        else:
            self.max = vmax
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_axes([0.1,0.1,.6,.6])
        self.axes2 = self.fig.add_axes([0.1,0.75,.8,.2])
        self.axes3 = self.fig.add_axes([0.75,0.15,0.075,0.5])
        self.axes2.hold(False)
        self.axes.hold(False)
        FigureCanvasQTAgg.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvasQTAgg.setSizePolicy(self,
                                        QtGui.QSizePolicy.Expanding,
                                        QtGui.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)
        self.matrix=matrix.reshape(self.x, self.y)
        self.compute_initial_figure()


    def new_data(self, matrix, scale):
        self.scale = scale
        self.matrix = matrix.reshape(self.x, self.y)
        if self.visual == Scans[2]:
            self.image.set_data(self.matrix)
            self.image.changed()
        elif self.visual == Scans[1]:
            matrix = self.matrix.flatten()
            self.axes.plot(matrix, "r-")
            self.axes.axis([0, len(matrix)-1, self.min, self.max])
        if self.scale=="linear":
            self.axes2.axis([0,
                             len(self.plot_matrix),
                             numpy.amin(self.plot_matrix),
                             numpy.amax(self.plot_matrix)])
            self.axes2.plot(self.energy_matrix, self.plot_matrix, "b-")
        else:
            self.axes2.axis([0, 2048, 1,1000])
            self.axes2.semilogy(self.energy_matrix, self.plot_matrix, "b-")
        self.axes2.set_xlabel("Energy")
        self.axes2.set_ylabel("Count")
        self.draw()

    def sizeHint(self):
        w, h = self.get_width_height()
        return QtCore.QSize(w, h)

    def minimumSizeHint(self):
        return QtCore.QSize(10, 10)

    def compute_initial_figure(self):
        if self.plot_matrix != None:
            if self.scale == "linear":
                self.axes2.axis([0,
                                 len(self.plot_matrix),
                                 numpy.amin(self.plot_matrix),
                                 numpy.amax(self.plot_matrix)])
                self.axes2.plot(self.energy_matrix, self.plot_matrix, "b-")
            else:
                self.axes2.axis([0, 2048, 1,1000])
                self.axes2.semilogy(self.energy_matrix, self.plot_matrix, "b-")
            self.axes2.set_xlabel("Energy")
            self.axes2.set_ylabel("Count")
        if self.visual == Scans[2]:
            self.image = self.axes.imshow(self.matrix,
                                          vmin=self.min,
                                          vmax=self.max,
                                          interpolation="nearest",
                                          origin="lower")
            self.cbar = self.fig.colorbar(self.image,self.axes3)
            matrix = self.matrix.flatten()
        elif self.visual == Scans[1]:
            matrix = self.matrix.flatten()
            self.axes.plot(matrix, "r-")
            self.axes.axis([0, len(matrix)-1, self.min, self.max])
        self.draw()
