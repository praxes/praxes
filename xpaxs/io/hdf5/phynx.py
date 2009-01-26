"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import operator
import os

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import numpy
import h5py

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

import phynx

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

mapdict = {
    'fitArea': ('fit', 'Fit'),
    'sigmaArea': ('fit_error', 'FitError'),
    'massFraction': ('mass_fraction', 'MassFraction')
}

def convert_entry(old, new):
    try:
        mon = old.attrs['skipmodeMonitor']
        thresh = old.attrs['skipmodeThresh']

        skipped = new['measurement']['scalar_data'][mon].value < thresh
        kwargs = {'attrs':{'class':'Signal', 'monitor':mon, 'threshold':thresh}}
        dset = scalar_data.create_dataset(
            'skipped', data=skipped, **kwargs
        )
    except:
        pass

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
                typename, cls = mapdict[mapType]
                element = '_'.join(
                    [element[:-1], element[-1], typename]
                )
                newMaps.create_dataset(
                    element,
                    type=cls,
                    data=map.value.flatten()
                )
    except:
        pass



def convert_to_phynx(
        spec_filename, h5_filename=None, oldh5_filename=None, force=False
    ):
    """convert a spec data file to phynx and return the phynx file object"""
    print 'Converting spec file %s to phynx'% spec_filename

    from xpaxs.io import spec
    f = spec.convert_to_phynx(spec_filename, h5_filename, force)

    if oldh5_filename is None:
        oldh5_filename = spec_filename + '.h5.old'
    if os.path.exists(oldh5_filename):
        oldf = h5py.File(oldh5_filename, 'r')
        edict = dict(
            [(entry.attrs['scan number'], entry)
                for entry in oldf.iterobjects()]
        )
        for k, oldentry in edict.iteritems():
            try:
                newentry = f['entry_%d'%k]
                convert_entry(oldentry, newentry)
            except:
                pass

    return f
