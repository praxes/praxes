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
import tables

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

mapdict = {
    'fitarea': ('fit', 'Fit'),
    'sigmaarea': ('fit_error', 'FitError'),
    'massfraction': ('mass_fraction', 'MassFraction')
}

def convert_entry(old, new):
    try:
        mca = new['measurement'].mcas.values()[0]
        mca.attrs['pymca_config'] = str(old._v_attrs.pymcaConfig)
    except:
        pass

    try:
        oldMaps = old.elementMaps
        newMaps = new['measurement'].create_group(
            'element_maps', type='ElementMaps'
        )
        for mapType in oldMaps:
            for map in mapType:
                element = map._v_name
                typename, cls = mapdict[mapType._v_name.lower()]
                element = '_'.join(
                    [element[:-1], element[-1], typename]
                )
                newMaps.create_dataset(
                    element,
                    type=cls,
                    data=map[:].flatten()
                )
    except:
        pass



def convert_to_phynx(
        spec_filename, h5_filename=None, oldh5_filename=None, force=False
    ):
    """convert a spec data file to phynx and return the phynx file object"""

    from xpaxs.io import spec
    f = spec.convert_to_phynx(spec_filename, h5_filename, force)

    if oldh5_filename is None:
        oldh5_filename = spec_filename + '.h5.old'
    if os.path.exists(oldh5_filename):
        oldf = tables.openFile(oldh5_filename, 'r')
        edict = dict(
            [(entry._v_attrs.scanNumber, entry)
                for entry in oldf.root]
        )

        for k, oldentry in edict.iteritems():
            try:
                newentry = f['entry_%d'%(int(k))]
                convert_entry(oldentry, newentry)
            except:
                pass

    return f
