"""
pychess.specfile is an interface to datafiles created by Certified
Scientific's spec program, which is commonly used in synchrotron labs.
pychess.specfile extends an established esrf library called SpecFile, which
is written in C, so it is very fast.

Use:

    >>> scanList = load('example.dat')

Each scan contains the data and a scan_info attribute for accessing information
stored in the scan header, like motor positions, scan parameters, etc.

"""

from __future__ import division
import os

from itertools import izip
import numpy

from PyMca import specfile
from pychess.specfile.mcdata import McaData, McsData
try: import tables
except ImportError: pass

__all__ = ['load']


class ChessSpecfile(object):

    """A thin wrapper of the ESRF's Specfile class"""

    def __init__(self, filename):
        """\
        filename:
            a string
        """
        self._filename = filename
        self._specfile = specfile.Specfile(filename)

    def __getitem__(self, index):
        try:
            scan = self._specfile[index]
        except IndexError:
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

        try:
            nb_mcas = self.scan_info.get_number_mcas()
        except specfile.error:
            nb_mcas = 0

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
        dev_info = self.scan_info.get_scan_header('@')
        nb_devices = self.scan_info.get_number_mcas()
        l = len(self.scan_info.get_mca(index))
        channels = [l, 0, l-1, 1]
        coeffs = [0, 1, 0]
        dev_name = 'MCA%d'% index

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
                break
    return scans

# and here is some code for converting to hdf5:

filters = tables.Filters(complib='zlib', complevel=9)

class Data(tables.IsDescription):
    pass

Data = {}

def convertScan(scan, sfile, h5file):
    scanEntry = h5file.createGroup('/', 'scan%d'%scan.number())
    
    
    attrs = scanEntry._v_attrs
    epoch = sfile.epoch()
    for motor, pos in zip(sfile.allmotors(), scan.allmotorpos()):
        setattr(attrs, motor, pos)
    
    labels = scan.alllabels()
    for label in labels:
#        setattr(Data, label, tables.Float32Col())
        Data[label] = tables.Float32Col()
    
    numMca = int(scan.nbmca()/scan.lines())
    # try to get MCA metadata:
    mcaInfo = scan.header('@')
    mcaNames = []
    if len(mcaInfo)/3 == numMca:
        for i in xrange(numMca):
            itemInfo, mcaInfo = mcaInfo[:3], mcaInfo[3:]
            mcaName = itemInfo[0].split()[0][2:]
            mcaNames.append(mcaName)
            start, stop, step = [int(i) for i in itemInfo[1].split()[2:]]
            channels = numpy.arange(start,  stop+1, step)
            energy = numpy.polyval([float(i) for i in itemInfo[2].split()[1:]],
                                   channels)
            
#            setattr(Data, mcaName, tables.Float32Col(shape=channels.shape))
            Data[mcaName] = tables.Float32Col(shape=channels.shape)
            
            mcaEntry = h5file.createGroup(scanEntry, mcaName)
            channelsEntry = h5file.createCArray(mcaEntry, 'channels',
                                                tables.UInt16Atom(),
                                                channels.shape, filters=filters)
            channelsEntry[:] = channels
            energyEntry = h5file.createCArray(mcaEntry, 'energy',
                                              tables.Float32Atom(),
                                              energy.shape, filters=filters)
            energyEntry[:] = energy
    else:
        print 'mca metadata in specfile is incomplete!'
        for i in xrange(numMca):
            mcaName = 'MCA%d'%i
            mcaNames.append(mcaName)
            temp = scan.mca(1)
            
            channels = numpy.arange(len(temp))
            energy = channels
            
#            setattr(Data, mcaName, tables.Float32Col(shape=channels.shape))
            Data[mcaName] = tables.Float32Col(shape=channels.shape)
            
            mcaEntry = h5file.createGroup(scanEntry, mcaName)
            channelsEntry = h5file.createCArray(mcaEntry, 'channels',
                                                tables.UInt16Atom(),
                                                channels.shape, filters=filters)
            channelsEntry[:] = channels
            energyEntry = h5file.createCArray(mcaEntry, 'energy',
                                              tables.Float32Atom(),
                                              energy.shape, filters=filters)
            energyEntry[:] = energy
    
    # create the table:
    dataTable = h5file.createTable(scanEntry, 'data', Data, filters=filters,
                                   expectedrows=scan.lines())
    
    for i in xrange(scan.lines()):
        row = dataTable.row
        for label, val in zip(labels, scan.dataline(i+1)):
            if label.lower() == 'epoch': val += epoch
            row[label] = val
        for j, label in enumerate(mcaNames):
            row[label] = scan.mca((numMca*i+1)+j)
        row.append()

def spec2hdf5(filename):
    """returns a pytables file object
    """
    h5filename = filename + '.h5'
    if os.path.exists(h5filename):
        h5file = tables.openFile(h5filename, 'r+')
    else:
        h5file = tables.openFile(h5filename, 'w')
        sfile = specfile.Specfile(filename)
        for scan in sfile:
            convertScan(scan, sfile, h5file)
        h5file.flush()
    return h5file
