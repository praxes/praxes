"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

from md5 import md5
import os
import subprocess
import sys

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import numpy as np
try:
    import specfile
except ImportError:
    from PyMca import specfile

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs.io.phynx import File

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

compression = {'compression':4, 'shuffle':True, 'fletcher32':True}

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
    elif scan_type in ('smesh', ):  # AW adds, 3/17/09
    # Example: smesh  scany 32.3 32.7 -0.05 0.15 100  scanx -143.5 -123.5 40  1
    #                       ^^^^ ^^^^ <- These are upper and lower limits and can be discarded
        args = args[:1] + args[3:]
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
            'ascan', 'a2scan', 'a3scan', 'dscan', 'd2scan', 'd3scan',
            'ztscan', 'ytscan', 'xtscan',
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
    scan_info['scan_shape'] = np.array(scan_info['scan_shape'][::-1])

    return scan_info

def process_mca(scan, measurement, process_scalars=False, masked=None):
    num_mca = int(scan.nbmca()/scan.lines())
    mca_info = scan.header('@')
    mca_names = []
    print 'Number of MCA:', num_mca
    for mca_index in xrange(num_mca):
        attrs = {}
        if len(mca_info)/3 == num_mca:
            item_info, mca_info = mca_info[:3], mca_info[3:]
            attrs['id'] = item_info[0].split()[0][2:]
            start, stop, step = [int(i) for i in item_info[1].split()[2:]]
            channels = np.arange(start,  stop+1, step)
            attrs['calibration'] = str(tuple(np.array(
                [float(i) for i in item_info[2].split()[1:]]
            )))
        else:
            print 'mca metadata in specfile is incomplete!'

            attrs['id'] = 'mca_%d'%mca_index
            channels = np.arange(len(scan.mca(1)))

        mca_names.append(attrs['id'])

        mca = measurement.create_group(
            attrs['id'], type='MultiChannelAnalyzer', **attrs
        )
        mca['channels'] = channels
        mca.create_dataset(
            'counts', type='McaSpectrum', dtype='float32', shape=(scan.lines(), len(channels))
        )

        buff = []
        thresh = 500
        for i in xrange(scan.lines()):
            buff.append(scan.mca(num_mca * i + 1 + mca_index)[:len(channels)])
            if len(buff) == thresh:
                mca['counts'][i+1-len(buff):i+1] = buff
                buff = []
                sys.stdout.write('.')
                sys.stdout.flush()
        else:
            if len(buff):
                mca['counts'][i+1-len(buff):i+1] = buff
                sys.stdout.write('.\n')
                sys.stdout.flush()

        if process_scalars:
            # assume all scalars to be signals, except dead_time
            for i, label in enumerate(scan.alllabels()):
                kwargs = {'class':'Signal'}
                if label == 'dead_time':
                    kwargs['class'] = 'DeadTime'
                    kwargs['units'] = '%'
                    kwargs['dead_time_format'] = '%'
                dset = mca.create_dataset(
                    label, data=scan.datacol(i+1), dtype='float32', **kwargs
                )

        if masked is not None:
            mca['masked'] = masked

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
    scan_name = scan_number

    print 'converting %s'% scan_name

    scan_info = get_spec_scan_info(scan.command().split())
    labels = [label.lower() for label in scan.alllabels()]
    # We need to update time metadata if it was a tseries:
    if scan_info['scan_type'] == 'tseries':
        scan_info['scan_shape'] = np.array([scan.lines()])
        # ugh;
        index = labels.index('time')+1
        t = scan.datacol(index)
        scan_info['axis_info']['time']['range'] = str((t.min(), t.max()))
    # We need to update time metadata if it was a chess_escan:
    if scan_info['scan_type'] == 'chess_escan':
        scan_info['scan_shape'] = np.array([scan.lines()])
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
            scan_info['scan_shape'] = np.array([scan.lines()])
    attrs['acquisition_shape'] = str(tuple(scan_info['scan_shape']))

    entry = h5file.create_group(scan_name, type='Entry', **attrs)

    measurement = entry.create_group('measurement', type='Measurement')

    positioners = measurement.create_group('positioners', type='Positioners')
    try:
        for motor, pos in zip(sfile.allmotors(), scan.allmotorpos()):
            positioners[motor] = pos
    except specfile.error:
        pass

    scalar_data = measurement.create_group('scalar_data', type='ScalarData')

    skipmode = scan.header('C SKIPMODE')
    if skipmode:
        mon, thresh = skipmode[0].split()[2:]
        thresh = int(thresh)
        index = scan.alllabels().index(mon)+1
        skipped = scan.datacol(index) < thresh
        kwargs = {'class':'Signal', 'monitor':mon, 'threshold':thresh}
        masked = scalar_data.create_dataset(
            'masked', data=skipped, **kwargs
        )
    else:
        masked = None

    # try to get MCA metadata:
    print 'processing MCA data ',
    try:
        mca = process_mca(scan, measurement, masked=masked)
    except specfile.error:
        mca = None
    sys.stdout.write('\n')
    sys.stdout.flush()

    try:
        allmotors = sfile.allmotors()
    except specfile.error:
        allmotors = []
    for i, label in enumerate(scan.alllabels()):
        if label in scalar_data:
            print 'Badly formatted spec file, %s appears more than once'%label
            continue
        if mca is not None and label in (
                    'icr', 'ocr', 'real', 'live', 'dtn', 'vtxdtn', 'dead',
                    'dead_time'
                ):
            # vortex detector, assume single mca
            kwargs = {'class':'Signal', 'signal':0}
            if label == 'dead_time':
                kwargs['units'] = '%'
                kwargs['class'] = 'DeadTime'
                kwargs['dead_time_format'] = '%'
            try:
                dset = mca.create_dataset(
                    label, data=scan.datacol(i+1), dtype='float32', **kwargs
                )
            except UnboundLocalError:
                dset = measurement.create_dataset(
                    label, data=scan.datacol(i+1), dtype='float32', **kwargs
                )
        elif (label in allmotors) \
            or (label.lower() in ('energy', 'time', 'h', 'k', 'l', 'q')):
            kwargs = {'class':'Axis'}
            kwargs.update(
                scan_info['axis_info'].get(label.lower(), {})
            )
            dset = scalar_data.create_dataset(
                label, data=scan.datacol(i+1), dtype='float32', **kwargs
            )
        elif label.lower() == 'epoch':
            kwargs = {'class':'Axis'}
            dset = scalar_data.create_dataset(
                label, data=scan.datacol(i+1)+sfile.epoch(), dtype='float32',
                **kwargs
            )
        else:
            kwargs = {'class':'Signal'}
            dset = scalar_data.create_dataset(
                label, data=scan.datacol(i+1), dtype='float32', **kwargs
            )
    # the last column should always be the primary counter
    dset.attrs['signal'] = 1

    # and dont forget to include the index
    kwargs = {'class':'Axis'}
    dset = scalar_data.create_dataset(
        'i', data=np.arange(len(dset)), dtype='i', **kwargs
    )

    dir, spec_filename = os.path.split(spec_filename)
    if not dir:
        dir = os.getcwd()
    for f in os.listdir(dir):
        # process mca device files:
        if (
            f.startswith(spec_filename+'.scan%s.'%scan_number) and
            f.endswith('.mca')
        ):
            print 'integrating %s'%f
            process_mca(
                specfile.Specfile(f)[0], measurement, True, masked=masked
            )
        elif (
            f.startswith(spec_filename+'.%s_'%scan_number) and
            f.endswith('.mar3450')
        ):
            try:
                p = subprocess.Popen(
                    ['marcvt', '-raw32', f],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                res = p.wait()
                raw = p.stdout.readline().split()[-1]
                d = np.fromfile(raw, dtype='uint32')
                os.remove(raw)
                d /= 2
                p = int(np.sqrt(len(d)))
                d.shape = (p, p)
                mar = measurement.require_group('mar345', type='Mar345')
                dset = mar.require_dataset(
                    'counts', shape=(scan.lines(), p, p), dtype='uint16'
                )
                i = f.replace(spec_filename+'.%s_'%scan_number, '')
                i = int(i.replace('.mar3450', ''))
                dset[i] = d
                if masked is not None and 'masked' not in mar:
                    mar['masked'] = masked
                print 'integrated %s' % f
            except:
                sys.stdout.write('Found mar image but unable to fetch it.')
                sys.stdout.write('Perhaps marcvt is not installed.')


def convert_to_phynx(spec_filename, h5_filename=None, force=False):
    """convert a spec data file to phynx and return the phynx file object"""
    print 'Converting spec file %s to phynx'% spec_filename
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
        try:
            scan.lines()
        except specfile.error:
            # scan.lines() failed because there were none
            continue
        convert_scan(scan, spec_file, h5_file, spec_filename)

    print 'phynx %s complete'% h5_file
    return h5_file
