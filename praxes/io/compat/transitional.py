"""
"""

import operator
import os

import h5py


mapdict = {
    'fitarea': ('fit', 'Fit'),
    'sigmaarea': ('fit_error', 'FitError'),
    'massfraction': ('mass_fraction', 'MassFraction')
}

def convert_entry(old, new):
    try:
        mca = new['measurement'].mcas.values()[0]

        mca.attrs['pymca_config'] = old.attrs['pymcaConfig']
    except:
        pass

    try:
        oldMaps = old['elementMaps']
        newMaps = new['measurement'].create_group('element_maps', type='ElementMaps')
        for mapType in oldMaps:
            for element, map in oldMaps[mapType].iteritems():
                typename, cls = mapdict[mapType.lower()]
                element = '_'.join(
                    [element[:-1], element[-1], typename]
                )
                newMaps.create_dataset(
                    element,
                    type=cls,
                    data=map[...].flatten()
                )
    except:
        pass



def convert_to_phynx(
        spec_filename, h5_filename=None, oldh5_filename=None, force=False
    ):
    """convert a spec data file to phynx and return the phynx file object"""

    from praxes.io.phynx.migration import spec
    f = spec.convert_to_phynx(spec_filename, h5_filename, force)

    if oldh5_filename is None:
        oldh5_filename = spec_filename + '.h5.old'
    if os.path.exists(oldh5_filename):
        oldf = h5py.File(oldh5_filename, 'r')
        try:
            edict = dict(
                [(entry.attrs['scan number'], entry)
                    for entry in oldf.itervalues()]
            )
        except h5py.H5Error:
            edict = dict(
                [(entry.attrs['scanNumber'], entry)
                    for entry in oldf.itervalues()]
            )

        for k, oldentry in edict.iteritems():
            try:
                newentry = f['entry_%d'%(int(k))]
                convert_entry(oldentry, newentry)
            except:
                pass

    return f
