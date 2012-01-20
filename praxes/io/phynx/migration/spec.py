"""
"""
from __future__ import absolute_import

import gc
from hashlib import md5
import os
import subprocess
import sys

import numpy as np

from praxes.io import spec
from .. import open


class ScanInfoParser(object):

    def __init__(self):
        self._parsers = {}

    def __getitem__(self, key):
        return self._parsers[key]

    def __setitem__(self, key, val):
        self._parsers[key] = val

    def __call__(self, args):
        scan_type = args.pop(0)
        info = {
            'scan_type': scan_type,
            'axes': [],
            'axis_info': {},
            'scan_shape': [],
            }

        try:
            scan_info = self[scan_type](info, *args)
            scan_info['scan_shape'] = np.array(scan_info['scan_shape'][::-1])
        except KeyError:
            raise RuntimeError('Scan %s not recognized!'%scan_type)

        return scan_info

get_scan_metadata = ScanInfoParser()

def _mesh(scan_info, *args):
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
    return scan_info
get_scan_metadata['mesh'] = _mesh
get_scan_metadata['zzmesh'] = _mesh

def _smesh(scan_info, *args):
    # Example: smesh  scany 32.3 32.7 -0.05 0.15 100  scanx -143.5 -123.5 40  1
    #                       ^^^^ ^^^^ <- These are upper and lower limits and
    #                       can be discarded
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
    return scan_info
get_scan_metadata['smesh'] = _smesh

def _1d(scan_info, *args):
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
    return scan_info
get_scan_metadata['ascan'] = _1d
get_scan_metadata['a2scan'] = _1d
get_scan_metadata['a3scan'] = _1d
get_scan_metadata['dscan'] = _1d
get_scan_metadata['d2scan'] = _1d
get_scan_metadata['d3scan'] = _1d
get_scan_metadata['ztscan'] = _1d
get_scan_metadata['ytscan'] = _1d
get_scan_metadata['xtscan'] = _1d

def _tseries(scan_info, *args):
    numPts = int(args[0])
    if numPts < 1:
        numPts = -1
    try:
        ctime = float(args[1])
    except IndexError:
        ctime = 1.0
    scan_info['axes'].append('time')
    axis_info = {}
    axis_info['axis'] = 1
    axis_info['range'] = str((0, ctime*numPts))
    scan_info['axis_info']['time'] = axis_info
    scan_info['scan_shape'].append(numPts)
    return scan_info
get_scan_metadata['tseries'] = _tseries

def _escan(scan_info, *args):
    start, stop, steps = args[:3]
    start, stop, steps = float(start), float(stop), int(steps)+1
    scan_info['axes'].append('energy')
    axis_info = {}
    axis_info['axis'] = 1
    axis_info['range'] = str((start, stop))
    scan_info['axis_info']['energy'] = axis_info
    scan_info['scan_shape'].append(steps)
    return scan_info
get_scan_metadata['Escan'] = _escan

def _chess_escan(scan_info, *args):
    scan_info['axes'].append('energy')
    axis_info = {}
    axis_info['axis'] = 1
    scan_info['axis_info']['energy'] = axis_info
    return scan_info
get_scan_metadata['chess_escan'] = _chess_escan


def process_mca(scan, measurement, masked=None, report=False):
    mca_info = scan.attrs['mca_info']
    num_mca = len(mca_info)
    npoints = measurement.entry.npoints

    monitor = scan.attrs.get('monitor', None)
    monitor_efficiency = scan.attrs.get('monitor_efficiency', 1)
    try:
        dead_time_format = [i for i in scan.attrs['user_comments']
                            if i.startswith('dead_time format')][0].split()[-1]
    except IndexError:
        dead_time_format = "percent"

    try:
        fast_dead_time = [i for i in scan.attrs['user_comments']
                          if i.startswith('DXP fast_dead_time')][0].split()[-1]
        fast_dead_time = float(fast_dead_time)
    except IndexError:
        fast_dead_time = 0

    if report: print 'Number of MCA:', num_mca
    keys = [i for i in scan.keys() if i.startswith('@')]
    for key in keys:
        val = scan[key]
        key = key[1:] # drop the @

        attrs = {}
        if monitor:
            attrs['monitor'] = monitor

        attrs['fast_dead_time'] = fast_dead_time

        try:
            attrs.update(mca_info[key])
            attrs['id'] = key
            start, stop, step = attrs['channels'][1:]
            channels = np.arange(start,  stop+1, step)
            attrs['calibration'] = str(attrs['calibration'])
        except KeyError:
            if report: print 'mca metadata in specfile is incomplete!'
            attrs['id'] = key
            channels = np.arange(len(val[0]))

        mca = measurement.create_group(
            attrs['id'], type='MultiChannelAnalyzer', **attrs
            )
        mca['channels'] = channels
        mca.create_dataset(
            'counts',
            type='Spectrum',
            dtype='float32',
            shape=(npoints, len(channels))
            )

        buff = []
        thresh = 500
        for i in xrange(len(val)):
            buff.append(val[i])
            if len(buff) == thresh:
                mca['counts'][i+1-len(buff):i+1] = buff
                buff = []
                if report: sys.stdout.write('.')
                if report: sys.stdout.flush()
        else:
            if len(buff):
                mca['counts'][i+1-len(buff):i+1] = buff
                if report: sys.stdout.write('.\n')
                if report: sys.stdout.flush()


            # assume all scalars to be signals, except dead_time
        for key, val in scan.items():
            if key.startswith('@'):
                continue
            kwargs = {'class':'Signal'}
            if key == 'dead_time':
                kwargs['class'] = 'DeadTime'
                kwargs['dead_time_format'] = dead_time_format
            if key == monitor:
                kwargs['efficiency'] = monitor_efficiency
            dset = mca.create_dataset(
                key, shape=(npoints,), dtype='float32', **kwargs
                )
            dset[:len(val)] = val

        if masked is not None:
            mca['masked'] = masked

    try:
        if report: sys.stdout.write('\n')
        if report: sys.stdout.flush()
        return mca
    except UnboundLocalError:
        pass

def convert_scan(scan, h5file, spec_filename, report=False):
    # access a bunch of metadata before creating an hdf5 group
    # if specfile raises an error because the scan is empty,
    # we will skip it and move on to the next

    if report: print 'converting scan #%s'% scan.name

    scan_info = get_scan_metadata(scan.attrs['command'].split())
    labels = [label.lower() for label in scan.keys()]
    # We need to update time metadata if it was a tseries:
    if scan_info['scan_type'] == 'tseries':
        scan_info['scan_shape'] = np.array([len(scan.values()[0])])
        t = scan['Time'][:]
        scan_info['axis_info']['time']['range'] = str((t.min(), t.max()))
    # We need to update time metadata if it was a chess_escan:
    if scan_info['scan_type'] == 'chess_escan':
        scan_info['scan_shape'] = np.array([len(scan.values()[0])])
        e = scan['energy'][:]
        scan_info['axis_info']['energy']['range'] = str((e.min(), e.max()))

    attrs = {}
    attrs['acquisition_name'] = scan.name
    attrs['acquisition_id'] = scan.id
    attrs['npoints'] = len(scan.values()[0])
    attrs['acquisition_command'] = scan.attrs['command']
    attrs['source_file'] = scan.attrs['file_origin']

    if len(scan_info['scan_shape']) < 2:
        if scan_info['scan_shape'] < 1:
            # an open-ended scan
            scan_info['scan_shape'] = np.array([len(scan.values()[0])])
    attrs['acquisition_shape'] = str(tuple(scan_info['scan_shape']))

    entry = h5file.create_group(scan.id, type='Entry', **attrs)

    measurement = entry.create_group('measurement', type='Measurement')

    positioners = measurement.create_group('positioners', type='Positioners')
    for motor, pos in scan.attrs['positions'].items():
        try:
            positioners[motor] = pos
        except ValueError:
            if report: print (
    """
    Invalid spec motor configuration:
    "%s" is used to describe more than one positioner.
    Only the first occurance will be saved. Please report
    the problem to your beamline scientist
    """ % motor
            )

    attrs = {}

    monitor = scan.attrs['monitor']
    if monitor:
        attrs['monitor'] = monitor
    scalar_data = measurement.create_group(
        'scalar_data', type='ScalarData', **attrs
        )

    skipmode = [i for i in scan.attrs['comments'] if i.startswith('SKIPMODE')]
    if not skipmode:
        skipmode = [i for i in scan.attrs['user_comments']
                    if i.startswith('SKIPMODE')]
    if skipmode:
        mon, thresh = skipmode[0].split()[2:]
        thresh = int(thresh)
        skipped = scan[mon][:] < thresh
        kwargs = {'class':'Signal', 'counter':mon, 'threshold':thresh}
        masked = scalar_data.create_dataset(
            'masked', dtype='uint8', data=skipped.astype('uint8'), **kwargs
        )
    else:
        masked = None

    allmotors = scan.attrs['positions'].keys()
    for key, val in scan.items():
        if key.startswith('@') or key in scalar_data:
            continue

        val = val[:]
        if (key in allmotors) \
            or (key.lower() in ('energy', 'time', 'h', 'k', 'l', 'q')):
            kwargs = {'class':'Axis'}
            kwargs.update(
                scan_info['axis_info'].get(key.lower(), {})
                )
            dset = scalar_data.create_dataset(
                key, data=val, dtype='float32', **kwargs
                )
        elif key.lower() == 'epoch':
            kwargs = {'class':'Axis'}
            dset = scalar_data.create_dataset(
                key,
                data=val+scan.attrs['epoch_offset'],
                dtype='float64',
                **kwargs
                )
        else:
            kwargs = {'class':'Signal'}
            dset = scalar_data.create_dataset(
                key, data=val, dtype='float32', **kwargs
                )
    # the last column should always be the primary counter
    scalar_data[scan.attrs['labels'][-1]].attrs['signal'] = 1

    # and dont forget to include the index
    kwargs = {'class':'Axis'}
    dset = scalar_data.create_dataset(
        'i', data=np.arange(len(dset)), dtype='i', **kwargs
        )

    # process mca device files:
    if [i for i in scan.keys() if i.startswith('@')]:
        process_mca(scan, measurement, masked=masked)

    # we need to integrate external data files after processing the scan
    # in the main file, since we may reference some of that data
    dir, spec_filename = os.path.split(spec_filename)
    if not dir:
        dir = os.getcwd()
    for f in sorted(os.listdir(dir)):
        if (
            f.startswith(spec_filename+'.scan%s.'%scan.name) and
            f.endswith('.mca')
            ):
            f = os.path.join(dir, f)
            if report: print 'integrating %s'%f
            process_mca(
                spec.open(f)[scan.id], measurement, masked=masked
                )
        elif (
            f.startswith(spec_filename+'_scan%03d_'%(int(scan.name))) and
            f.endswith('.tiff')
            ):
            from praxes.io.tifffile import TIFFfile
            f = os.path.join(dir, f)
            d = TIFFfile(f).asarray()
            r, c = d.shape
            ad = measurement.require_group('area_detector', type='AreaDetector')
            dset = ad.require_dataset(
                'counts', (scan.lines(), r, c), 'uint32', maxshape=(None, r, c)
                )
            i = f.replace(spec_filename+'_scan%03d_'%(int(scan_number)), '')
            i = int(i.replace('.tiff', ''))
            try:
                dset[i] = d
            except:
                dset.resize((i, r, c))
                dset[i] = d
            del d
            try:
                line = [i for i in scan.attrs['comments']
                        if i.startswith('subexposures')][0]
                n = int(line.split()[1].split('=')[1])
                dset.attrs['subexposures'] = n
            except IndexError:
                pass
            if masked is not None and 'masked' not in ad:
                ad['masked'] = masked
            if report: print 'integrated %s' % f
            gc.collect()
        elif (
            f.startswith(spec_filename+'.%s_'%scan.name) and
            f.endswith('.mar3450')
            ):
            f = os.path.join(dir, f)
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
                del d
                if masked is not None and 'masked' not in mar:
                    mar['masked'] = masked
                if report: print 'integrated %s' % f
                gc.collect()
            except (OSError, ValueError):
                if report: sys.stdout.write(
                    'Found mar image %s but unable to convert it.\n' % f
                    )
                if report: sys.stdout.write(
                    'marcvt must be installed to do so.\n'
                    )


def convert_to_phynx(
    spec_filename, h5_filename=None, force=False, report=False
    ):
    """convert a spec data file to phynx and return the phynx file object"""
    if report: print 'Converting spec file %s to phynx'% spec_filename
    if h5_filename is None:
        h5_filename = spec_filename + '.h5'
    if os.path.exists(h5_filename) and force==False:
        raise IOError(
            '%s already exists! Use "force" flag to overwrite'%h5_filename
        )

    if report: print 'making file %s'% h5_filename
    h5_file = open(h5_filename, 'w')
    spec_file = spec.open(spec_filename)
    for scan in spec_file.values():
        if len(scan.values()[0]):
            convert_scan(scan, h5_file, spec_filename, report=report)

    if report: print 'phynx %s complete'% h5_file
    return h5_file
