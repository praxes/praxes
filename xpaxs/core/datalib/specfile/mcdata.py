"""The mcdata module is designed to provide a convenient and efficient
interface to multi-channel analyzer and multi-channel scalar data. When
a spec datafile is loaded, an interface is created to multi-channel devices
like multi-channel scalars and multi-channel analyzers. For example:

>>> from pychess import specfile
>>> scan1, = specfile.load('example.dat', 1)

At this point, an interface to an MCA device, called MCA0 in the specfile,
has automatically been created and can be accessed as scan1.MCA0. If the
calibration was set up properly in spec, then the energy can be read by
doing

>>> print scan1.MCA0.energy

If the energy was not calibrated in spec, you can calibrate it by doing

>>> scan1.MCA0.set_calibration([a,b,c])

where energy = a + b*X + c*X^2, and X is the channel number.

The MCA counts can be read by indexing MCA0. Get the first MCA0 scan:

>>> print scan1.MCA0.counts[0]

get the first 10 MCA0 scans

>>> print scan1.MCA0.counts[:10]

"""

import tempfile

import numpy


__all__ = []


class MultiChannelData(object):

    """An object-oriented interface to multi-channel data

    The object can be indexed to yield an array of multi-channel data,
    where each row represents a single multi-channel scan, with the counts
    stored in the columns.

    MultiChannelData is a base class, not intended to be used directly,
    but inherited by McaData and McsData.
    """

    def __init__(self, name, device_number, scan, channels, calibration):
        '''
        construct an interface to the data from a multi-channel device

        name:
            the name of the multichannel data (MCA0, MCA1, MCS0...)
        device_number:
            an index, the order in which the device is reported
        scan:
            the ChessScandata object containing the device
        channels:
            a list containing, in order:

              - the total number of channels
              - the start index
              - the stop index
              - the step size

        calibration: a list [a,b,c] used to scale the channels:

              -Y = aX**2 + bX + c

        '''
        self.name = name
        self._dev_nb = device_number
        self._scandata = scan
        self._mca = scan.scan_info.get_scandata().mca

        total, start, stop, step = channels
        self.channels = numpy.arange(start, stop+1, step, dtype=numpy.float64)
        self.set_calibration(calibration)

#        shape = scan.scan_info.scan_shape
#        shape = [numpy.product(shape)]
#        shape.append(len(self.channels))

        shape = [scan.scan_info.get_number_rows()]
        shape.append(len(self.channels))

        nb_mcas = scan.scan_info.get_number_mcas()
        dev_nb = self._dev_nb

        f = tempfile.NamedTemporaryFile()
        name = f.name
        f.close()

        self.counts = numpy.memmap(name, dtype=numpy.float64, mode='w+',
                                   shape=tuple(shape))

        for i in xrange(scan.scan_info.get_number_rows()):
            self.counts[i,:] = self._mca(dev_nb+nb_mcas*(i+1))

    def set_calibration(self, value):
        """
        set_calibration(array([a,b,c]))

        where Y = a + b*X + c*X^2

        X is the channel number, and Y is the calibrated scale
        """
        self._calibration = value[::-1]
        temp = self.channels
        self._scaled_channels = numpy.polyval(self._calibration, temp)


class McsData(MultiChannelData):

    """An object-oriented interface to multi-channel scalar data

    The object can be indexed to yield an array of multi-channel scalar
    data, where each row represents a single multi-channel scan, with the
    counts stored in the columns.

    The time is scaled using the "set_calibration" method, you can not
    alter the time directly.
    """

    def time():
        doc = """return the MCS_dwell*bin#"""
        def fget(self):
            return self._scaled_channels
        def fset(self, value):
            raise AttributeError, 'time can not be set. Use set_calibration instead'
        return locals()
    time = property(**time())


class McaData(MultiChannelData):

    """An object-oriented interface to multi-channel data

    The object can be indexed to yield an array of multi-channel data,
    where each row represents a single multi-channel scan, with the counts
    stored in the columns.

    The energy is scaled using the "set_calibration" method, you can not
    alter the energy directly.
    """

    def energy():
        doc = """return the calibrated MCA energy"""
        def fget(self):
            return self._scaled_channels
        def fset(self, value):
            raise AttributeError, 'energy can not be set. Use set_calibration instead'
        return locals()
    energy = property(**energy())
