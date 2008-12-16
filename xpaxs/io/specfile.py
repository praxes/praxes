"""
specfile is an interface to datafiles created by Certified
Scientific's spec program, which is commonly used in synchrotron labs.
pychess.specfile extends an established esrf library called SpecFile, which
is written in C, so it is very fast.

Use:

    >>> scanList = load('example.dat')

Each scan contains the data and a scan_info attribute for accessing information
stored in the scan header, like motor positions, scan parameters, etc.

"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

from __future__ import division
from itertools import izip
import logging
import os
import tempfile

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import numpy

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

# TODO: fix this import:
from PyMca.specfile import Specfile, Scandata, error

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

logger = logging.getLogger('XPaXS.io.specfile')

__all__ = ['load']

def getScanInfo(commandList):
    scan_type, args = commandList[0], commandList[1:]
    scan_info = {}
    scan_info['scan_type'] = scan_type
    scan_info['axes'] = []
    scan_info['axis_info'] = {}
    scan_info['scan_shape'] = []
    if scan_type in ('mesh', ):
        i = 0
        while len(args) > 4:
            (axis, start, stop, step), args = args[:4], args[4:]
            start, stop, step = float(start), float(stop), int(step)+1
            i += 1
            scan_info['axes'].append((axis, ))
            axis_info = {}
            axis_info['range'] = numpy.array([start, stop])
            axis_info['axis'] = i
            scan_info['axis_info'][axis] = axis_info
            scan_info['scan_shape'].append(step)
    elif scan_type in (
            'ascan', 'a2scan', 'a3scan', 'dscan', 'd2scan', 'd3scan'
        ):
        temp = []
        i = 0
        while len(args) > 3:
            (axis, start, stop), args = args[:3], args[3:]
            start, stop = float(start), float(stop)
            i += 1
            temp.append(axis)
            axis_info = {}
            axis_info['axis'] = 1
            axis_info['priority'] = i
            axis_info['range'] = numpy.array([start, stop])
            scan_info['axis_info'][axis] = axis_info
        scan_info['axes'].append(tuple(temp))
        scan_info['scan_shape'].append(int(args[0])+1)
    elif scan_type in ('tseries', ):
        numPts = int(args[0])
        if numPts < 1: numPts = -1
        try: ctime = float(args[1])
        except IndexError: ctime = 1.0
        scan_info['axes'].append('time')
        axis_info = {}
        axis_info['axis'] = 1
        axis_info['range'] = numpy.array([0, ctime*numPts])
        scan_info['axis_info']['time'] = axis_info
        scan_info['scan_shape'].append(numPts)
    elif scan_type in ('Escan', ):
        start, stop, steps = args[:3]
        start, stop, steps = float(start), float(stop), int(steps)+1
        scan_info['axes'].append('energy')
        axis_info = {}
        axis_info['axis'] = 1
        axis_info['range'] = numpy.array([start, stop])
        scan_info['axis_info']['energy'] = axis_info
        scan_info['scan_shape'].append(steps)
    else:
        raise RuntimeError('Scan %s not recognized!'%commandType)
    scan_info['scan_shape'] = numpy.array(scan_info['scan_shape'][::-1])

    return scan_info


class ChessSpecfile(object):

    """A thin wrapper of the ESRF's Specfile class"""

    def __init__(self, filename):
        """\
        filename:
            a string
        """
        self._filename = filename
        self._specfile = Specfile(filename)

    def __getitem__(self, index):
        try:
            scan = self._specfile[index]
        except IndexError:
            logger.error('index %d out of bounds', index)
            raise IndexError, 'index %d out of bounds'% index
        return ChessScandata(scan, self)

    def get_date(self):
        """return a string, the date the file was created"""
        return self._specfile.date()

    def get_epoch_offset(self):
        """return the epoch offset"""
        return self._specfile.epoch()

    def get_esrf_specfile(self):
        """return the ESRF Specfile instance, primarily for debugging"""
        return self._specfile

    def get_filename(self):
        """return a string, the filename"""
        return self._filename

    def get_motor_names(self):
        """return a list of motornames"""
        return self._specfile.allmotors()

    def get_scan(self, scan_number, scan_order=1):
        """return a ChessScandata instance

        scan_number:
            the number of the scan
        scan_order:
            an index indicating whether to return the first, second, etc.
            occurance of a scan labeled as scan_number. scan_order is necessary
            because it is possible to have more than one scan labeled as scan X
            in a single spec datafile
        """
        try:
            scan = self._specfile.select('%d.%d'%(scan_number, scan_order))
        except specfile.error:
            logger.error('scan %d:%d not found', scan_order, scan_number)
            raise specfile.error, 'scan %d:%d not found'% \
                (scan_order, scan_number)
        return scan

    def get_scan_list(self):
        """return a list of scans in the spec datafile"""
        return self._specfile.list()

    def get_title(self):
        """return a string, the title of the spec geometry code"""
        return self._specfile.title()

    def get_user(self):
        """return a string, the user ID"""
        return self._specfile.user()

    def update(self):
        return self._specfile.update()


class ChessScanInfo(object):

    """A thin wrapper around the ESRF Scandata object"""

    def __init__(self, scan, file):
        """\
        scan:
            an ESRF Scandata instance
        file:
            a ChessSpecfile instance
        """
        self._specfile = file
        self._scandata = scan

#        cmd = scan.command().split()
#        isascan = cmd[0] in ['ascan', 'dscan']
#        if not isascan and cmd[0] != 'mesh':
#            raise TypeError, 'Scan %d in %s is not a mesh|ascan|dscan (it\'s a %s)' % \
#                  (self.get_scan_number(), self.get_specfile(), cmd[0])
#        goodlen = (isascan and 6) or 10
#        if len(cmd) != goodlen:
#            raise SyntaxError, 'Invalid command:' % scan.command()
#
#        self.fast_motor, fstart, fend, fnpts = cmd[1:5]
#        if isascan:
#            self.slow_motor, sstart, send, snpts = 'None', 0, 0, 0
#        else:
#            self.slow_motor, sstart, send, snpts = cmd[5:9]
#
#        self.integration_time = float(cmd[-1])
#
#        pos = map(float, [fstart, fend, sstart, send])
#        self.fast_lims = pos[:2]
#        self.slow_lims = pos[2:]
#        fnpts, snpts = map(int, [fnpts, snpts])
#
#        pixel_x = abs(self.fast_lims[0] - self.fast_lims[1]) / fnpts
#        if isascan:
#            pixel_y = 0
#        else:
#            pixel_y = abs(self.slow_lims[0] - self.slow_lims[1]) / snpts
#
#        fnpts += 1
#        snpts += 1
#
#        npts = self.get_number_rows()
#        if npts < snpts * fnpts:
#            expect = snpts
#            snpts = (npts + fnpts - 1) / fnpts
#            print 'Warning: scan has only %d lines (instead of %d)' % (snpts, expect)
#
#        self.scan_shape = [snpts, fnpts]

    def get_all_labels(self):
        """return a list of scan data labels"""
        return self._scandata.alllabels()

    def get_all_motor_positions(self):
        """return a dictionary of motor positions at start of scan"""
        pos = {}
        for label, value in izip(self._specfile.allmotors(),
                                 self._scandata.allmotorpos()):
            pos[label] = value
        return pos

    def get_column(self, index):
        """return a data column

        index:
            an integer between 0 and the number of columns-1 in the scan
        """
        return self._scandata.datacol(index+1)

    def get_command(self):
        """return a string showing the scan command"""
        return self._scandata.command()

    def get_data(self):
        """return an array containing all the scalar data"""
        return self._scandata.data()

    def get_date(self):
        """return the date the scan was run"""
        return self._scandata.date()

    def get_epoch_offset(self):
        """return a number

        the epoch offset is a number subtracted from the epochs in the scan
        data
        """
        return self._specfile.get_epoch_offset()

    def get_file_header(self):
        return self._scandata.fileheader()

    def get_scan_header(self, headerItem=''):
        """return the scan header information

        headerItem:
            a string. If defined, return the specific header information. If
            undefined or an empty string, return the whole header
        """
        return self._scandata.header(filter)

    def get_hkl(self):
        """return an array of <HKL> values"""
        return self._scandata.hkl()

    def get_mca(self, index):
        """return an array of MCA data

        index:
            an integer
        """
        return self._scandata.mca(index+1)

    def get_motor_position(self, motor):
        """returns the motor position at start of scan"""
        return self._scandata.motorpos(motor)

    def get_number_columns(self):
        """return the number of columns of scan data"""
        return self._scandata.cols()

    def get_number_rows(self):
        """return the number of rows of scan data"""
        return self._scandata.lines()

    def get_number_mcas(self):
        """return the number of MCAs"""
        lines = self._scandata.lines()
        nbmca = self._scandata.nbmca()
        return int(nbmca/lines) # **-1?

    def get_row(self, index):
        """return a data row

        index:
            an integer
        """
        return self._scandata.dataline(index+1)

    def get_scandata(self):
        """return the esrf Scandata object"""
        return self._scandata

    def get_scan_number(self):
        """return the scan number"""
        return self._scandata.number()

    def get_scan_order(self):
        """return an integer

        the scan order is an index indicating if this is the first, second, ...
        time this scan number has appeared in the spec datafile. Consider it a
        bug in spec that multiple scans can be labeled as scan #1 in the same
        file.
        """

    def get_specfile(self):
        """return the ChessSpecfile object"""
        return self._specfile


class ChessScandata(object):

    """A convenient interface to spec datafiles"""

    def __init__(self, scan, file):
        """\
        scan:
            an ESRF Scandata instance
        file:
            a ChessSpecfile instance
        """
        self.scan_info = ChessScanInfo(scan, file)
        logger.debug('scan info: %s', self.scan_info)
        try:
            nb_mcas = self.scan_info.get_number_mcas()
        except specfile.error:
            nb_mcas = 0
        logger.debug('number mcas = %s', nb_mcas)

        for i in xrange(nb_mcas):
            self._add_mc_device(i)

        try:
            data = self.scan_info.get_data()
            for label, value in izip(self.scan_info.get_all_labels(),
                                     self.scan_info.get_data()):
                setattr(self, label, numpy.array(value))
                if label.lower() == 'epoch':
                    epoch_offset = self.scan_info.get_epoch_offset()
                    setattr(self, label, numpy.array(value)+epoch_offset)
        except specfile.error:
            # TODO: is this necessary?
            pass

    def _add_mc_device(self, index):
        """add multi-channel device data instance to the scan data

        index:
            an integer
        """
        logger.debug('Adding mc device')
        dev_info = self.scan_info.get_scan_header('@')
        nb_devices = self.scan_info.get_number_mcas()
        l = len(self.scan_info.get_mca(index))
        channels = [l, 0, l-1, 1]
        coeffs = [0, 1, 0]
        dev_name = 'MCA%d'% index
        logger.debug(dev_info)
        logger.debug('Number MCAS: %s', nb_devices)

        found = 0
        for line in dev_info:
            flag, info = line.split(None, 1)
            flag = flag[2:]
            if flag == 'CHANN':
                if found == index:
                    # total, start, stop, step:
                    channels = [int(i) for i in info.split()[-4:]]
            elif flag == 'CALIB':
                if found == index:
                    coeffs = [float(i) for i in info.split()[-3:]]
                    break
                else:
                    found += 1
            elif found == index:
                dev_name = flag

        if 'MCA' in dev_name:
            setattr(self, dev_name, McaData(dev_name, index, self, channels, coeffs))
        elif 'MCS' in dev_name:
            setattr(self, dev_name, McsData(dev_name, index, self, channels, coeffs))
        else:
            setattr(self, dev_name, MultiChannelData(dev_name, index, self, channels, coeffs))


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



def load(filename, *scans, **kwargs):
    '''
    Return a list of scans.

    filename:
        a string
    scans:
        integers indicatng which scans to load. If no scans are indicated,
        load every scan in the file.

    Examples:

        >>> scanList = load("example.dat")

        >>> scan1, scan5 = load("example.dat", 1, 5)

    If no scan indices are given, returns every scan present in the file. Each
    scan contains the data and a scan_info attribute for accessing information
    stored in the scan header.

    '''
    logger.debug('Loading File: %s', filename)
    sf = ChessSpecfile(datafile)
    if args:
        scans = [ChessScandata(sf.get_scan(arg), sf) for arg in args]
    else:
        scans = []
        index = 0
        while 1:
            try:
                scans.append(sf[index])
                index += 1
            except IndexError:
                logger.error('Index error at index %s', index)
                break
    return scans
