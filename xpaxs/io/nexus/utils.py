"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os

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

__all__ = ['load']

# and here is some code for converting to hdf5:
compression = {'compression':9, 'shuffle':True, 'fletcher32':True}

def get_spec_scan_info(commandList):
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
    elif scan_type in ('chess_escan', ):
        scan_info['axes'].append('energy')
        axis_info = {}
        axis_info['axis'] = 1
        scan_info['axis_info']['energy'] = axis_info
    else:
        raise RuntimeError('Scan %s not recognized!'%scan_type)
    scan_info['scan_shape'] = numpy.array(scan_info['scan_shape'][::-1])

    return scan_info

def convert_scan(scan, sfile, h5file):
    # access a bunch of metadata before creating an hdf5 group
    # if specfile raises an error because the scan is empty,
    # we will skip it and move on to the next

    file_name = scan.fileheader('F')[0].split()[1]
    scan_number = '%d.%d'%(scan.number(), scan.order())
    scan_number = scan_number.replace('.1', '')
    scan_name = 'entry'+scan_number

    print 'Converting Spec File %s %s to h5'% (file_name, scan_name)

    scan_info = get_spec_scan_info(scan.command().split())
    # We need to update time metadata if it was a tseries:
    if scan_info['scan_type'] == 'tseries':
        scan_info['scan_shape'] = numpy.array([scan.lines()])
        # ugh;
        index = scan.alllabels().index('Time')+1
        t = scan.datacol(index)
        scan_info['axis_info']['time']['range'] = \
            numpy.array([t.min(), t.max()])
    if scan_info['scan_type'] == 'chess_escan':
        scan_info['scan_shape'] = numpy.array([scan.lines()])
        # ugh
        index = scan.alllabels().index('Energy')+1
        t = scan.datacol(index)
        scan_info['axis_info']['energy']['range'] = \
            numpy.array([t.min(), t.max()])

    attrs = {}
    attrs['scan_number'] = scan_number
    attrs['scan_lines'] = scan.lines()
    attrs['scan_command'] = scan.command()
#    attrs['scan_type'] = scanType
    attrs['scan_axes'] = scan_info['axes']
#    attrs['scanRange'] = scanRange

    if scan_info['scan_shape'] < 1:
        scan_info['scan_shape'] = numpy.array([scan.lines()])
    attrs['entry_shape'] = scan_info['scan_shape']

    entry = h5file.create_group(scan_name, type='Entry', attrs=attrs)
    print 'creating group %s'% scan_name

    instrument = entry.create_group('instrument', type='Instrument')
    motors = instrument.create_group('motors', type='Group')
    for motor, pos in zip(sfile.allmotors(), scan.allmotorpos()):
        motors[motor] = pos

    measurement = entry.create_group('measurement', type='Data')

#    skipmode = scan.header('C SKIPMODE')
#    if skipmode:
#        skipmodeMonitor, skipmodeThresh = skipmode[0].split()[2:]
#        skipmodeThresh = int(skipmodeThresh)
#    else:
#        skipmodeMonitor, skipmodeThresh = None, 0

#    if skipmodeMonitor:
#        attrs.skipmodeMonitor = skipmodeMonitor
#        attrs.skipmodeThresh = skipmodeThresh

    # try to get MCA metadata:
    print 'Getting MCA Metadata'

    num_mca = int(scan.nbmca()/scan.lines())
    mca_info = scan.header('@')
    mca_names = []
    for mca_index in xrange(num_mca):
        attrs = {}
        if len(mca_info)/3 == num_mca:
            item_info, mca_info = mca_info[:3], mca_info[3:]
            attrs['id'] = item_info[0].split()[0][2:]
            start, stop, step = [int(i) for i in item_info[1].split()[2:]]
            channels = numpy.arange(start,  stop+1, step)
            attrs['calibration'] = numpy.array(
                [float(i) for i in item_info[2].split()[1:]]
            )
        else:
            print 'mca metadata in specfile is incomplete!'

            attrs['id'] = 'MCA%d'%mca_index
            channels = numpy.arange(len(scan.mca(1)))

        mca_names.append(attrs['id'])

        mca = measurement.create_group(
            attrs['id'], type='MultiChannelAnalyzer', attrs=attrs
        )
        mca['channels'] = channels
        mca.create_dataset(
            'counts', dtype='float32', shape=(scan.lines(), len(channels)),
            **compression
        )

        for line in xrange(scan.lines()):
            mca['counts'][line] = scan.mca((num_mca*line+1)+mca_index)

    allmotors = sfile.allmotors()
    for i, label in enumerate(scan.alllabels()):
        if label in ('icr', 'ocr', 'real', 'live', 'dtn', 'vtxdtn'):
            # vortex detector, assume single mca
            try:
                dset = mca.create_dataset(
                    label, data=scan.datacol(i+1), dtype='float32',
                    **compression
                )
                if label in ('dtn', 'vtxdtn'):
                    mca.attrs['deadtime_correction'] = label
            except UnboundLocalError:
                dset = measurement.create_dataset(
                    label, data=scan.datacol(i+1), dtype='float32',
                    **compression
                )
        elif label in allmotors:
            kwargs = {'attrs': {'axis':0}}
            kwargs['attrs'].update(scan_info['axis_info'].get(label, {}))
            kwargs.update(compression)
            dset = measurement.create_dataset(
                label, data=scan.datacol(i+1), dtype='float32', **kwargs
            )
        elif label.lower() == 'epoch':
            kwargs = {'attrs': {'axis':0}}
            kwargs.update(compression)
            dset = measurement.create_dataset(
                label, data=scan.datacol(i+1)+sfile.epoch(), dtype='float32',
                **kwargs
            )
        else:
            kwargs = {'attrs': {'signal':0}}
            kwargs.update(compression)
            dset = measurement.create_dataset(
                label, data=scan.datacol(i+1), dtype='float32', **kwargs
            )
    # the last column should always be the primary counter
    dset.attrs['signal'] = 1

def convert_spec(spec_filename, h5_filename=None, force=False):
    """convert a spec data file to hdf5 and return the file object"""
    print 'Converting spec file %s to hdf5'% spec_filename
    if h5_filename is None:
        h5_filename = spec_filename + '.h5'
    if os.path.exists(h5_filename) and force==False:
        raise IOError('%s already exists! Use force flag to overwrite'%h5_filename)

    from .file import File as H5File

    print 'making file %s'% h5_filename
    h5_file = H5File(h5_filename, 'w')
    spec_file = Specfile(spec_filename)
    for scan in spec_file:
        'converting Scan %s'% scan
        convert_scan(scan, spec_file, h5_file)
    print 'h5file %s complete'% h5_file
    return h5_file
