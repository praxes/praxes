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
#try:
#    import specfile
#except ImportError:
#    from PyMca import specfile
from PyMca import specfile

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from ..file import File

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

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
            axis_info['range'] = str((start, stop))
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
            axis_info['primary'] = i
            axis_info['range'] = str((start, stop))
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
        axis_info['range'] = str((0, ctime*numPts))
        scan_info['axis_info']['time'] = axis_info
        scan_info['scan_shape'].append(numPts)
    elif scan_type in ('Escan', ):
        start, stop, steps = args[:3]
        start, stop, steps = float(start), float(stop), int(steps)+1
        scan_info['axes'].append('energy')
        axis_info = {}
        axis_info['axis'] = 1
        axis_info['range'] = str((start, stop))
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

def process_mca(scan, measurement, process_scalars=False):
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
            attrs['calibration'] = str(tuple(numpy.array(
                [float(i) for i in item_info[2].split()[1:]]
            )))
        else:
            print 'mca metadata in specfile is incomplete!'

            attrs['id'] = 'mca_%d'%mca_index
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
            mca['counts'][line] = scan.mca((num_mca*line+1) \
                + mca_index)[:len(channels)]

        if process_scalars:
            # assume all scalars to be signals
            for i, label in enumerate(scan.alllabels()):
                kwargs = {'attrs': {'class':'Signal'}}
                kwargs.update(compression)
                dset = mca.create_dataset(
                    label, data=scan.datacol(i+1), dtype='float32', **kwargs
                )

    try:
        return mca
    except UnboundLocalError:
        pass

def convert_scan(scan, sfile, h5file, spec_filename):
    # access a bunch of metadata before creating an hdf5 group
    # if specfile raises an error because the scan is empty,
    # we will skip it and move on to the next

    file_name = scan.fileheader('F')[0].split()[1]
    scan_number = '%d.%d'%(scan.number(), scan.order())
    scan_number = scan_number.replace('.1', '')
    scan_name = 'entry_'+scan_number

    print 'Converting Spec File %s %s to h5'% (file_name, scan_name)

    scan_info = get_spec_scan_info(scan.command().split())
    labels = [label.lower() for label in scan.alllabels()]
    # We need to update time metadata if it was a tseries:
    if scan_info['scan_type'] == 'tseries':
        scan_info['scan_shape'] = numpy.array([scan.lines()])
        # ugh;
        index = labels.index('time')+1
        t = scan.datacol(index)
        scan_info['axis_info']['time']['range'] = str((t.min(), t.max()))
    # We need to update time metadata if it was a chess_escan:
    if scan_info['scan_type'] == 'chess_escan':
        scan_info['scan_shape'] = numpy.array([scan.lines()])
        # ugh
        index = labels.index('energy')+1
        t = scan.datacol(index)
        scan_info['axis_info']['energy']['range'] = str((t.min(), t.max()))

    attrs = {}
    attrs['acquisition_name'] = scan_name
    attrs['acquisition_id'] = scan_number
    attrs['npoints'] = scan.lines()
    attrs['acquisition_command'] = scan.command()
#    attrs['scan_type'] = scanType
#    attrs['scan_axes'] = scan_info['axes']
#    attrs['scanRange'] = scanRange

    if len(scan_info['scan_shape']) < 2:
        if scan_info['scan_shape'] < 1:
            # an open-ended scan
            scan_info['scan_shape'] = numpy.array([scan.lines()])
    attrs['acquisition_shape'] = str(tuple(scan_info['scan_shape']))

    entry = h5file.create_group(scan_name, type='Entry', attrs=attrs)
    print 'creating group %s'% scan_name

    measurement = entry.create_group('measurement', type='Measurement')

    positioners = measurement.create_group('positioners', type='Positioners')
    try:
        for motor, pos in zip(sfile.allmotors(), scan.allmotorpos()):
            positioners[motor] = pos
    except specfile.error:
        pass

    # try to get MCA metadata:
    print 'Getting MCA Metadata'

    mca = process_mca(scan, measurement)

    scalar_data = measurement.create_group('scalar_data', type='ScalarData')

    try:
        allmotors = sfile.allmotors()
    except specfile.error:
        allmotors = []
    for i, label in enumerate(scan.alllabels()):
        if mca is not None and \
            label in ('icr', 'ocr', 'real', 'live', 'dtn', 'vtxdtn'):
            # vortex detector, assume single mca
            kwargs = {'attrs': {'class':'Signal', 'signal':0}}
            kwargs.update(compression)
            try:
                dset = mca.create_dataset(
                    label, data=scan.datacol(i+1), dtype='float32',
                    **kwargs
                )
                if label in ('dtn', 'vtxdtn'):
                    mca.attrs['deadtime_correction'] = label
            except UnboundLocalError:
                dset = measurement.create_dataset(
                    label, data=scan.datacol(i+1), dtype='float32',
                    **kwargs
                )
        elif (label in allmotors) \
            or (label.lower() in ('energy', 'time', 'h', 'k', 'l', 'q')):
            kwargs = {'attrs': {'class':'Axis'}}
            kwargs['attrs'].update(
                scan_info['axis_info'].get(label.lower(), {})
            )
            kwargs.update(compression)
            dset = scalar_data.create_dataset(
                label, data=scan.datacol(i+1), dtype='float32', **kwargs
            )
        elif label.lower() == 'epoch':
            kwargs = {'attrs': {'class':'Axis'}}
            kwargs.update(compression)
            dset = scalar_data.create_dataset(
                label, data=scan.datacol(i+1)+sfile.epoch(), dtype='float32',
                **kwargs
            )
        else:
            kwargs = {'attrs': {'class':'Signal'}}
            kwargs.update(compression)
            dset = scalar_data.create_dataset(
                label, data=scan.datacol(i+1), dtype='float32', **kwargs
            )
    # the last column should always be the primary counter
    dset.attrs['signal'] = 1

    # and dont forget to include the index
    kwargs = {'attrs': {'class':'Axis'}}
    kwargs.update(compression)
    dset = scalar_data.create_dataset(
        'i', data=numpy.arange(len(dset)), dtype='i', **kwargs
    )

    skipmode = scan.header('C SKIPMODE')
    if skipmode:
        mon, thresh = skipmode[0].split()[2:]
        thresh = int(thresh)
        index = scan.alllabels().index(mon)+1
        skipped = scan.datacol(index) < thresh
        kwargs = {'attrs':{'class':'Signal', 'monitor':mon, 'threshold':thresh}}
        kwargs.update(compression)
        dset = scalar_data.create_dataset(
            'skipped', data=skipped, **kwargs
        )

    for f in os.listdir(os.curdir):
        print f, spec_filename+'.scan%s'%scan_number
        if f.startswith(spec_filename+'.scan%s'%scan_number) and \
            f.endswith('.mca'):
            process_mca(specfile.Specfile(f)[0], measurement, True)

def convert_spec(spec_filename, h5_filename=None, force=False):
    """convert a spec data file to hdf5 and return the file object"""
    print 'Converting spec file %s to hdf5'% spec_filename
    if h5_filename is None:
        h5_filename = spec_filename + '.h5'
    if os.path.exists(h5_filename) and force==False:
        raise IOError(
            '%s already exists! Use "force" flag to overwrite'%h5_filename
        )

    print 'making file %s'% h5_filename
    h5_file = File(h5_filename, 'w')
    spec_file = specfile.Specfile(spec_filename)
    for scan in spec_file:
        'converting Scan %s'% scan
        convert_scan(scan, spec_file, h5_file, spec_filename)
    print 'h5file %s complete'% h5_file
    return h5_file
