import operator
import os
import time

import h5py
import matplotlib
import numpy
from PyMca5.PyMcaPhysics.xrf import Elements as PyMEl
# TODO: whats this doing here?:
import pylab

global XRFALLOWED
try:
    from .xrf_analysis import *
    XRFALLOWED=True
except:
    XRFALLOWED=False
from .xrd_math_fcns import *
from .xrd_diffraction_conversion_fcns import *
from .XRDdefaults import *
from .xrf_depprof import *


#import Elemental
#class atabclass(tables.IsDescription):
#    qqpkind = tables.UInt16Col() #indeces of qqpktab
#    qqaqqind = tables.UInt16Col()   # the qqpk is at a position a,b in the qq map. these give a and b in units of indeces of qq
#    qqbqqind = tables.UInt16Col()
#    qqaiind = tables.Float32Col()  #same as above but in units of ifnnn (coordinate in qq)
#    qqbiind = tables.Float32Col()
#    iinda = tables.Float32Col() #indeces of ifnnn  (coordinate in ifnnn)
#    iindb = tables.Float32Col()
#    kinda = tables.UInt16Col() #indeces of knnn  (coordinate in ifnnn but represented by the peak index)
#    kindb = tables.UInt16Col()
#    delsig = tables.Float32Col()
#    deliind = tables.Float32Col()
#    qqpkvol = tables.Float32Col()
#    qqpknorm = tables.Float32Col()
#
#class qqpktabclass(tables.IsDescription):
#    qqindhigh = tables.UInt16Col()
#    qqindlow = tables.UInt16Col()
#    qqindlowmin = tables.UInt16Col()
#    qqindlowmax = tables.UInt16Col()
#    qqindhighmin = tables.UInt16Col()
#    qqindhighmax = tables.UInt16Col()
#    lowminbool = tables.BoolCol()
#    lowmaxbool = tables.BoolCol()
#    highminbool = tables.BoolCol()
#    highmaxbool = tables.BoolCol()
#    qqpkintensity = tables.Float32Col()
#    qqpkvolume = tables.Float32Col()
#    qqpknorm = tables.Float32Col()
##
def readh5pyarray(arrpoint):
    return eval('arrpoint'+('['+':,'*len(arrpoint.shape))[:-1]+']')

def readblin(h5mar, bin=0):
    bs=['blin0', 'blin1']
    if bin:
        bs=[b+'bin%d' %bin for b in bs]
    return numpy.array([readh5pyarray(h5mar[b]) for b in bs]), numpy.array([h5mar[b].attrs['weights'][:] for b in bs]).T

def getimapqgrid(chessh5dsetstr, imap=True,  qgrid=True, bin=0):
    h5chess=CHESSRUNFILE()
    imappoint=h5chess[chessh5dsetstr]
    temp=tuple()
    if imap:
        if bin==0:
            temp+=(readh5pyarray(imappoint),)
        else:
            temp+=(readh5pyarray(h5chess[chessh5dsetstr+('bin%d' %bin)]),)
    if qgrid:
        temp+=(imappoint.attrs['qgrid'], )
    h5chess.close()
    if len(temp)==1:
        return temp[0]
    return temp

def getchimapchigrid(chessh5dsetstr, chimap=True, chigrid=True, bin=0):
    h5chess=CHESSRUNFILE()
    chimappoint=h5chess[chessh5dsetstr]
    temp=tuple()
    if chimap:
        if bin==0:
            temp+=(readh5pyarray(chimappoint),)
        else:
            temp+=(readh5pyarray(h5chess[chessh5dsetstr+('bin%d' %bin)]),)
    if chigrid:
        temp+=(chimappoint.attrs['chigrid'], )
    h5chess.close()
    if len(temp)==1:
        return temp[0]
    return temp

def getkillmap(chessh5dsetstr, bin=0):
    h5chess=CHESSRUNFILE()
    if 'killmap' in chessh5dsetstr.rpartition('/')[2]:
        if bin==0:
            temp=numpy.bool_(readh5pyarray(h5chess[chessh5dsetstr]))
        else:
            temp=numpy.bool_(readh5pyarray(h5chess[chessh5dsetstr+('bin%d' %bin)]))
    else:
        print 'KILLMAP NOT FOUND> USING DEFAULT'
        xrdname='mar345'
        p=chessh5dsetstr.rpartition('/')[0]
        while p in h5chess: #this is to try to get the right detector but include backwards compatib lity from when 'xrdname' didn't exist
            if 'xrdname' in h5chess[p].attrs:
                xrdname=h5chess[p].attrs['xrdname']
                break
            p=p.rpartition('/')[0]

        if bin==0:
            temp=numpy.bool_(readh5pyarray(h5chess[xrdname+'killmap']))
        else:
            temp=numpy.bool_(readh5pyarray(h5chess[xrdname+'killmapbin%d' %bin]))
    h5chess.close()
    return temp

def getdqchiimage(chessh5dsetstr, bin=0):
    h5chess=CHESSRUNFILE()
    if bin==0:
        temp=readh5pyarray(h5chess[chessh5dsetstr])
    else:
        temp=readh5pyarray(h5chess[chessh5dsetstr+('bin%d' %bin)])
    h5chess.close()
    return temp


def labelnumberformat(x):
    if x>=1000 or x<.001:
        a="%.*e" % (3, x)
        a=a.replace('+','')
        b,c,d=a.partition('e')
        d=d.replace('0','')
        return ''.join((b,c,d))
    else:
        return "%.*g" % (3, x)

def qqpktuplist_h5qqpktab(qqpktab,qqnormcritval=0.0):
    return [([arow['qqindhigh'], arow['qqindlow'], arow['qqindlowmin'], arow['qqindlowmax'], arow['qqindhighmin'], arow['qqindhighmax'], arow['lowminbool'], arow['lowmaxbool'], arow['highminbool'], arow['highmaxbool']], [arow['qqpkintensity'], arow['qqpkvolume'], arow['qqpknorm']]) for arow in qqpktab.where('qqpknorm>=qqnormcritval')]

def updatelog(h5group, string):
    h5group.attrs['modifiedlog']='\n'.join((string, h5group.attrs['modifiedlog']))

def writeattr(h5path, h5groupstr, attrdict):
    """h5path must exist, write attr dict as individiual attrs in h5groupstr"""

    h5file=h5py.File(h5path, mode='r+')
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
    #node=h5file[h5groupstr]
    for key, val in attrdict.iteritems():
        h5analysis.attrs[key]=val
    if not ('modifiedlog' in h5analysis.attrs):
        h5analysis.attrs['modifiedlog']=''.join(('modifiedlog created ',  time.ctime()))
    updatelog(h5analysis,  ''.join(('DAQ attribute dictionary updated. background is ',attrdict['bcknd'],'. ',  time.ctime())))

    h5file.close()

def getbin(h5an):
    h5mar=h5an[getxrdname(h5an)]
    bin=1
    for name in h5mar.listnames():
        if name.startswith('countsbin'):
            bin=eval(name.partition('countsbin')[2])
            break
    return bin

getxrdname=lambda h5an: ('xrdname' in h5an.attrs.keys() and h5an.attrs['xrdname']) or 'mar345'

def getattr(h5path, h5groupstr):
    h5file=h5py.File(h5path, mode='r')
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
    attrdict={}
    keys=['pointlist', 'command', 'xgrid', 'zgrid', 'wavelength', 'cal', 'alpha', 'counter', 'elements', 'bcknd', 'chessrunstr', 'imapstr', 'chimapstr', 'killmapstr', 'qimagestr', 'chiimagestr', 'dqchiimagestr', 'x', 'z', 'acquisition_time', 'acquisition_shape', 'xrdname', 'psize', 'bin']
    for key in keys:
        if key in h5analysis.attrs:
            attrdict[key]=h5analysis.attrs[key]
    if (not 'psize' in attrdict.keys()) and ('chessrunstr' in attrdict.keys()):
        h5chess=CHESSRUNFILE()
        h5grp=h5chess[attrdict['chessrunstr']]
        attrdict['psize']=h5grp.attrs['psize']
        h5chess.close()
    h5file.close()
    return attrdict

def getdefaultscan(h5path):
    h5file=h5py.File(h5path, mode='r')
    if 'defaultscan' in h5file.attrs:
        temp=h5file.attrs['defaultscan']
    else:
        temp=None
    h5file.close()
    return temp

def ReadGunPropDict(h5analysis):#h5analysis must be the anlaysis group of an open h5
    if not ('depprof' in h5analysis):
        return None
    h5depprof=h5analysis['depprof']
    d={}
    for key in h5depprof.attrs.keys():
        d[key]=h5depprof.attrs[key]
    return d


def numpts_attrdict(attrdict):
    if 'acquisition_shape' in attrdict:
        return numpy.prod(numpy.uint16(attrdict['acquisition_shape']))
    #below should not be necessary
    if 'mesh' in attrdict['command']:
        return int(round(attrdict['xgrid'][2]*attrdict['zgrid'][2]))
    else:
        return int(round(max(attrdict['xgrid'][2], attrdict['zgrid'][2])))

def calcbcknd(h5path, h5groupstr, bcknd, bin=3, critfrac=0.05, weightprecision=0.01, normrank=0.5):
    """groupstr is to the main scan group,  e.g. XRD.PrimDataset. bcknd starts with 'min' or 'ave'"""
    print 'calculating ',  bcknd, ' background on ', h5path, h5groupstr
    h5file=h5py.File(h5path, mode='r+')
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
    h5mar=h5file['/'.join((h5groupstr, 'analysis', getxrdname(h5analysis)))]
    h5marcounts=h5file['/'.join((h5groupstr,'measurement', getxrdname(h5analysis), 'counts'))]
    pointlist=h5analysis.attrs['pointlist']
    shape=(h5marcounts.shape[1], h5marcounts.shape[2])
    

    if bin!=0:
        binshape=(shape[0]//bin, shape[1]//bin)

    if 'min' in bcknd:
        bcknddata=h5marcounts[pointlist[0], :, :]
        if 'bmin' in h5mar:
            del h5mar['bmin']
        if ('bminbin%d' %bin) in h5mar:
            del h5mar[('bminbin%d' %bin)]
        percind=max(1, int(round(len(pointlist)*critfrac)))
        if percind+1>=len(pointlist):
            print 'something bad might be about to happend because you have asked for too high of a percentile'
        if percind!=1:
            bcknddata=numpy.empty((percind+1, shape[0], shape[1]), dtype=h5marcounts.dtype)
    elif bcknd=='ave':
        bcknddata=numpy.zeros(shape,dtype='float32')
        if 'bave' in h5mar:
            del h5mar['bave']
        if ('bavebin%d' %bin) in h5mar:
            del h5mar[('bminbin%d' %bin)]

    if 'lin' in bcknd:
        data=h5marcounts[pointlist, :, :]
        killmap=getkillmap(h5analysis.attrs['killmapstr'])
        b0=readh5pyarray(h5mar['blin0'])
        f0vals=h5mar['blin0'].attrs['trialimageweights'][:]
        b1=readh5pyarray(h5mar['blin1'])
        f1vals=h5mar['blin1'].attrs['trialimageweights'][:]
        ans=FindLinearSumBcknd(data, killmap, b0, b1, f0vals, f1vals, fraczeroed=critfrac, rankfornorm=normrank, fprecision=weightprecision)
        for nam, wt, bn in zip(['blin0', 'blin1'], ans, [b0, b1]):
            h5ar=h5mar[nam]
            weights=numpy.zeros(h5marcounts.shape[0], dtype='float32')
            weights[pointlist]=wt
            h5ar.attrs['zerofrac']=critfrac
            h5ar.attrs['weightprecision']=weightprecision
            h5ar.attrs['normrank']=normrank
            h5ar.attrs['weights']=weights
            if bin!=0:
                binnam='%sbin%d' %(nam, bin)
                if binnam in h5mar:
                    del h5mar[binnam]
                h5arbin=h5mar.create_dataset(binnam, data=binimage(bn, bin))
                for key, val in h5ar.attrs.iteritems():
                    h5arbin.attrs[key]=val

    else:
        for count, pointind in enumerate(pointlist):
            print pointind

            data=h5marcounts[pointind, :, :]

            if 'min' in bcknd:
                if percind==1:
                    indeces=data<bcknddata
                    bcknddata[indeces]=data[indeces]
                else:
                    if count<=percind:
                        bcknddata[count, :, :]=data
                        if count==percind:
                            bcknddata=numpy.sort(bcknddata, axis=0)
                    else:
                        bcknddata[percind, :, :]=data
                    bcknddata=numpy.sort(bcknddata, axis=0)
                    if pointind==pointlist[-1]:
                        bcknddata=bcknddata[-2, :, :]
            elif bcknd=='ave':
                bcknddata+=data

        if len(pointlist)==0:
            print 'background calculation error: NO IMAGES FOUND'
            h5file.close()
        else:
            for dset in h5mar.iterobjects():
                if isinstance(dset, h5py.Dataset) and (('b'+bcknd) in dset.name.rpartition('/')[2]):
                    del dset #deletes the array about to be created and its derivatives
            if 'min' in bcknd:
                bminpoint=h5mar.create_dataset('bmin', data=bcknddata)
                bminpoint.attrs['percentile']=critfrac
                if bin!=0:
                    h5mar.create_dataset('bminbin%d' %bin, data=binimage(bcknddata, bin))
            elif bcknd=='ave':
                bcknddata=numpy.array(round(bcknddata/len(pointlist)), dtype=h5marcounts.dtype)
                h5mar.create_dataset('bave', data=bcknddata)
                if bin!=0:
                    h5mar.create_dataset('bavebin%d' %bin, data=binimage(bcknddata, bin))

        print bcknd[:3] ,' background calculation complete'
        if bin==0:
            t1=''
        else:
            t1=' and binned'
        updatelog(h5analysis,  ''.join(('dataset background calculated', t1, ': ', bcknd, '. finished ', time.ctime())))
        h5file.close()
        if bcknd=='minanom':
            calcbanom(h5path, h5groupstr, bqgrid=None, bin=bin)


def integrate(h5path, h5groupstr, singleimage=None, bckndbool=True, ):#singleimage is a string that is an index of marcounts or a string for other dataset or 'banom#'. only marcounts can get backnd subtraction
    performed=True
    h5file=h5py.File(h5path, mode='r')
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
    h5mar=h5file['/'.join((h5groupstr, 'analysis', getxrdname(h5analysis)))]

    imap, qgrid=getimapqgrid(h5analysis.attrs['imapstr'])
    dqchiimage=getdqchiimage(h5analysis.attrs['dqchiimagestr'])
    slots=numpy.uint16(qgrid[2])
    killmap=getkillmap(h5analysis.attrs['killmapstr'])
    normalizer=integrationnormalization(killmap, imap, dqchiimage, slots)

    imap*=killmap
    bcknd='no bcknd'
    if bckndbool:
        attrdict=getattr(h5path, h5groupstr)
        bcknd=attrdict['bcknd']
        if 'lin' in bcknd:
            bckndarr, blinwts=readblin(h5mar)
        else:
            bstr=''.join(('b', bcknd[:3]))
            if bstr in h5mar:
                bckndarr=readh5pyarray(h5mar[bstr])
                if bcknd=='minanom':
                    bminanomf=readh5pyarray(h5mar['bminanomf'])
            else:
                print 'Aborting: INTEGRATION ABORTED: CANNOT FIND ', bstr
                return 'Aborting: INTEGRATION ABORTED: CANNOT FIND ', bstr

    h5file.close()

    h5file=h5py.File(h5path, mode='r+')
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
    h5mar=h5file['/'.join((h5groupstr, 'analysis', getxrdname(h5analysis)))]
    h5marcounts=h5file['/'.join((h5groupstr,'measurement', getxrdname(h5analysis), 'counts'))]

    data=None
    if singleimage is not None:
        if singleimage.isdigit():
            pointlist=[eval(singleimage)]
        elif singleimage.startswith('banom'):
            data=h5mar['banom'][eval(singleimage[5:]), :, :]
        elif singleimage.startswith('raw'):
            data=h5marcounts[eval(singleimage[3:]), :, :]
        else:
            data=readh5pyarray(h5mar[singleimage])
    else:
        pointlist=h5analysis.attrs['pointlist']

    if not (data is None):
        if data.shape[0]<imap.shape[0]:
            if (imap.shape[0]%data.shape[0])!=0:
                h5file.close()
                print 'INTEGRATION ABORTED:',  numstr, " is bigger than or incommensurate with imap"
                return 'INTEGRATION ABORTED:',  numstr, " is bigger than or incommensurate with imap"
            data=unbinimage(data, imap.shape[0]/data.shape[0])
        savearr=normalizer*intbyarray(data, imap, dqchiimage, slots)
        savename='i%s' %singleimage
        if savename in h5mar:
            del h5mar[savename]
        h5mar.create_dataset('i%s' %singleimage, data=savearr)
        pointlist=[]
    else:
        if 'icounts' in h5mar:
            del h5mar['icounts']
        icounts=h5mar.create_dataset('icounts', data=numpy.zeros((h5marcounts.shape[0], qgrid[2]), dtype='float32'))
        icounts.attrs['qgrid']=qgrid

    for pointind in pointlist:

        print pointind

        data=h5marcounts[pointind, :, :]

        if data.shape[0]<imap.shape[0]:
            if (imap.shape[0]%data.shape[0])!=0:
                h5file.close()
                print 'INTEGRATION ABORTED:',  numstr, " is bigger than or incommensurate with imap"
                return 'INTEGRATION ABORTED:',  numstr, " is bigger than or incommensurate with imap"
            data=unbinimage(data, imap.shape[0]/data.shape[0])

        if bckndbool:
            if bcknd=='minanom':
                if bminanomf[pointind, 0]<0:
                    h5file.close()
                    print 'no calculation of bminanom background on the fly for integration'
                    return 'no calculation of bminanom background on the fly for integration'
                else:
                    banom=h5mar['banom'][pointind, :, :]
                    data=bckndsubtract(data, bckndarr, killmap, btype=bcknd, banom_f_f=(banom, bminanomf[pointind, 0], bminanomf[pointind, 1]))[0]
            elif 'lin' in bcknd:
                data=bckndsubtract(data, bckndarr, killmap, btype=bcknd, linweights=blinwts[pointind])[0]
            else:
                data=bckndsubtract(data, bckndarr, killmap, btype=bcknd)[0]

        icounts[pointind, :]=normalizer*intbyarray(data, imap, dqchiimage, slots)[:]


    if singleimage is not None:
        t2=singleimage
    else:
        t2='entire pointlist'
    updatelog(h5analysis,  ''.join(('image integration with ', bcknd, ': ', t2, '. finished ', time.ctime())))
    h5file.close()

def qqcalc(h5path,  h5groupstr, qgrid, image): #assume q interval is integral number of  1d int interval (imap qgrid)
    h5file=h5py.File(h5path, mode='r')
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
    h5mar=h5file['/'.join((h5groupstr, 'analysis', getxrdname(h5analysis)))]

    numstrlist=None

    singleimage=False
    if 'icounts' in image:
        counts=readh5pyarray(h5mar['icounts'])
    elif 'ifcounts' in image:
        counts=readh5pyarray(h5mar['ifcounts'])
    else:
        h5file.close()
        print "qqcalc aborted. don't understand image parameter"
        return "qqcalc aborted. don't understand image parameter"
    pointlist=h5analysis.attrs['pointlist']


    iqgrid=h5mar['icounts'].attrs['qgrid']
    h5file.close()

    imin,  imax,  iint=minmaxint_qgrid(iqgrid)
    qqmin,  qqmax,  qqint=minmaxint_qgrid(qgrid)
    if imin>qqmin:
        qgrid[2]-=(imin-qqmin)//qqint
        qgrid[0]=imin
    qqmin,  qqmax,  qqint=minmaxint_qgrid(qgrid)
    if imax<qqmax:
        qgrid[2]-=numpy.ceil((qqmax-imax)/qqint)
    qqmin,  qqmax,  qqint=minmaxint_qgrid(qgrid)
    indlow=numpy.uint16((qqmin-imin)/iint)
    indhigh=numpy.uint16(iqgrid[2]-(imax-qqmax)/iint)
    indratio=numpy.uint16(qqint/iint)
    indarray=numpy.array(range(indlow, indhigh, indratio))
    print 'qgrid ',  qgrid, ' length ', indarray.size
    qqshape=(qgrid[2], qgrid[2])


    h5file=h5py.File(h5path, mode='r+')
    if 'qqcounts' in h5mar:
        del h5mar['qqcounts']
    qqcounts=h5mar.create_dataset('qqcounts', (icounts.shape[0], qqshape[0], qqshape[1]), dtype='float32')
    qqmap=numpy.zeros(qqshape, dtype='float32')
    for pointind in range(icounts.shape[0]):
        qqcounts[pointind, :, :]=qqmap[:, :]
    qqcounts.attrs['qgrid']=qgrid

    for pointind in pointlist:
        print pointind
        qqtemp=qq_gen(counts[pointind, indarray])
        qqcounts[pointind, :, :]=qqtemp[:, :]
        qqmap+=qqtemp

    if 'qq' in h5mar:
        del h5mar['qq']
    qq=h5mar.create_dataset('qq', data=numpy.float32(qqmap/(1.0*len(pointlist))))
    qq.attrs['qgrid']=qgrid

    updatelog(h5analysis,  ''.join(('qq calculation: ', image.partition(' ')[0], '. finished ', time.ctime())))
    h5file.close()


def buildintmap(chessh5grpstr, qgrid, bin=3):
    h5chess=CHESSRUNFILE()
    h5grp=h5chess[chessh5grpstr]

    qimage=readh5pyarray(h5grp['qimage'])
    h5chess.close()

    imap=imap_gen(qimage, qgrid)

    imapname=','.join(tuple([labelnumberformat(num) for num in qgrid]))
    h5chess=CHESSRUNFILE('r+')
    h5grp=h5chess[chessh5grpstr+'/imap']
    if imapname in h5grp:
        del h5grp[imapname]
    dset=h5grp.create_dataset(imapname, data=imap)
    dset.attrs['qgrid']=qgrid
    h5grp.create_dataset(imapname+('bin%d' %bin), data=binimage(imap, bin=bin, zerokill=True))
    h5chess.close()

def buildchimap(chessh5grpstr, chigrid, bin=3):
    h5chess=CHESSRUNFILE()
    h5grp=h5chess[chessh5grpstr]

    qimage=readh5pyarray(h5grp['qimage'])
    chiimage=readh5pyarray(h5grp['chiimage'])

    h5chess.close()

    chimap=chimap_gen(qimage, chiimage, chigrid)

    chimapname=','.join(tuple([labelnumberformat(num) for num in chigrid]))
    h5chess=CHESSRUNFILE('r+')
    h5grp=h5chess[chessh5grpstr+'/chimap']
    if chimapname in h5grp:
        del h5grp[chimapname]
    if chimapname+('bin%d' %bin) in h5grp:
        del h5grp[chimapname+('bin%d' %bin)]
    dset=h5grp.create_dataset(chimapname, data=chimap)
    dset.attrs['chigrid']=chigrid
    h5grp.create_dataset(chimapname+('bin%d' %bin), data=binimage(chimap, bin=bin, zerokill=True))
    h5chess.close()

def calcqchiimages(chessh5grpstr, alsocalcbin=3):
    bin=1
    if bin>1:
        alsocalcbin=None
        onlybinsavestr='bin%d' %bin
    else:
        onlybinsavestr=''
    h5chess=CHESSRUNFILE()
    h5grp=h5chess[chessh5grpstr]
    imageshape=h5grp.attrs['detectorshape'][::-1]
    cal=h5grp.attrs['cal']
    fit2dcenter=cal[:2]
    alpharad=h5grp.attrs['alpha']*numpy.pi/180.
    L=cal[2]
    wl=h5grp.attrs['wavelength']
    psize=h5grp.attrs['psize']
    tiltdir=h5grp.attrs['tiltdirection']
    if 'xrdname' in h5grp.attrs:
        xrdname=h5grp.attrs['xrdname']
    else:
        xrdname='mar345'
    h5chess.close()

    center=centerindeces_fit2dcenter(fit2dcenter, detsize=imageshape[0])
    center, imageshape = tiltdirectionoperation(center, imageshape, tiltdir)

    center=numpy.uint16(numpy.round(numpy.float32(bincenterind_centerind(center, bin))))
    sizex=imageshape[0]//bin
    sizey=imageshape[1]//bin
    c=int(round(center[1]))
    if c>=sizey-1-c:
        leftisbig=True
    else:
        leftisbig=False
        c=sizey-1-c #this effectively reverse direction of the bincenter if closer to LHS than RHS
    sizey=c+1 #this is the size of the qchidimage. the size of the expanded image will be 2*(c)+1
    xvals=(numpy.float32(range(sizex))-center[0])*bin*psize
    yvals=numpy.float32(range(sizey))*bin*psize #these have units of mm (rho in x^ and y^ directions)
    rsq=(bin*psize*sizey)**2

    qimage=numpy.float32([[[q_rhosq(x**2+y**2, L, wl)*((x**2+y**2)<=rsq), azimuth_coords(x,y)] for y in yvals] for x in xvals])

    azimimage=qimage[:, :, 1]

    qimage=qimage[:, :, 0]
    inds=numpy.where(qimage>0)
    chiimage=numpy.zeros(qimage.shape, dtype='float32')
    chiimage[inds]=chi_q_azim(qimage[inds], azimimage[inds], alpharad, L, wl)
    print 'alpharad, L, wl', alpharad, L, wl
    chipos=chiimage[chiimage>0]
    print 'chiminmax', numpy.min(chipos), numpy.max(chipos)
    dqchiimage=numpy.zeros(qimage.shape, dtype='float32')
    dqchiimage[inds]=numpy.abs(dqchiperpixel(qimage[inds], chiimage[inds], azimimage[inds], alpharad, L, wl, binpsize=psize*bin))

    #used to not save azim. now save it as well as 2 others.
    twothetaimage=numpy.zeros(qimage.shape, dtype='float32')
    twothetaimage[inds]=twotheta_q(qimage[inds], wl, units='rad')
    polfactimage=numpy.zeros(qimage.shape, dtype='float32')
    polfactimage[inds]=polarizfactor_q_twotheta_azim(qimage[inds], twothetaimage[inds], azimimage[inds], wl)
    SiASFimage=numpy.zeros(qimage.shape, dtype='float32')
    SiASFimage[inds]=Si_atomsensfact(twothetaimage[inds], wl)


    fullsizeimage=numpy.zeros(imageshape, dtype='float32')
    smallwidth=imageshape[1]-sizey

    h5chess=CHESSRUNFILE('r+')
    circkillmap=readh5pyarray(h5chess[xrdname+'killmap'])
    h5grp=h5chess[chessh5grpstr]
    imls=[(qimage,'qimage'), (chiimage,'chiimage'), (dqchiimage,'dqchiimage'), (twothetaimage, 'twothetaimage'), (azimimage, 'azimimage'), (polfactimage, 'polfactimage'), (SiASFimage, 'SiASFimage')]
    for im, name in imls:
        if name=='chiimage' and not leftisbig:
            negatesmall=-1
        else:#else includes all other arrays
            negatesmall=1
        fullsizeimage[:, :smallwidth]=im[:, smallwidth-1::-1]*negatesmall   #   smallwidth-1::-1  gives smallwidth indeces
#        if name=='chiimage':
#            negatesmall*=-1
        fullsizeimage[:, smallwidth:]=im[:, :]
        fullsizeimage*=circkillmap
        if leftisbig:
            fullsizeimage=fullsizeimage[:,::-1] #CANNOT say fullsizeimage[:,:]= becuase hits creates a mirror

        fullsizeimage=tiltdirectioninverseoperation(fullsizeimage, tiltdir)
        if name+onlybinsavestr in h5grp:
            del h5grp[name+onlybinsavestr]
        dset=h5grp.create_dataset(name+onlybinsavestr, data=fullsizeimage)
        if not (alsocalcbin is None):
            name+='bin%d' %(alsocalcbin)
            binnedimage=binimage(fullsizeimage, bin=alsocalcbin, zerokill=True)
            if name in h5grp:
                del h5grp[name]
            h5grp.create_dataset(name, data=binnedimage)
    h5chess.close()





def writenumtotxtfile(runpath,  xvals, yvals, savename,  header=None):
#xvals and yvals must be arrays
    if header is not None:
        writestr=''.join((header, '\n'))
    else:
        writestr=''
    for i in range(xvals.size):
        writestr=''.join((writestr,'%f' %xvals[i], '\t',  '%f' %yvals[i], '\n'))
    filename=os.path.join(runpath,''.join((name, '.txt'))).replace('\\','/')
    filename=os.path.join(runpath,''.join((savename, '.txt'))).replace('\\','/')
    fout = open(filename, "w")
    fout.write(writestr)
    fout.close()

def writeplotso(runpath,  xvals, yvals, attrdict, xtype, savename):  #xvals and yvals must be same length numpy arrays, savename is filename without extension
    writestr=plotsoheader(attrdict, xtype)
    arg=numpy.argsort(xvals)
    xvals=xvals[arg]
    yvals=yvals[arg]
    for i in range(xvals.size):
        sigdig=7
        yv=yvals[i]
        if yv==0:
            yv+=10**(-1*sigdig)
        try:
            writestr=''.join((writestr,'%.6f' %xvals[i], ' ',  eval(''.join(("'%.","%d" %(numpy.abs(sigdig-numpy.ceil(numpy.log10(yv)))),"f' %yv"))), '\n'))
        except:
            print ''.join(("'%.","%d" %(numpy.abs(sigdig-numpy.ceil(numpy.log10(yv)))),"f' %yv"))
        #the 7 in above line gives 7 significant digits, the precision of float32
    filename=os.path.join(runpath,''.join((savename, '.plt'))).replace('\\','/')
    fout = open(filename, "w")
    fout.write(writestr)
    fout.close()

def writeall2dimages(runpath, h5path,  h5groupstr,  type, typestr, colorrange=None,  datsave=False,  extrabin=1):
    h5file=h5py.File(h5path, mode='r')
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
    h5mar=h5file['/'.join((h5groupstr, 'analysis', getxrdname(h5analysis)))]

    savename1='_'.join((os.path.split(h5path)[1][0:-3], h5groupstr, typestr, ''))

    pointlist=h5analysis.attrs['pointlist']
    bcknd=h5analysis.attrs['bcknd']
    usebanom=(type>0 and bcknd=='minanom') or (type==3)
    if usebanom:
        bminanomf=h5mar['bminanomf']
    if type>0:
        killmapbin=getkillmap(h5analysis.attrs['killmapstr'], bin=3)
        if extrabin>1:
            killmapbin=binboolimage(killmapbin, bin=extrabin)
    if type==1 or type==3 or type==4:
        if 'min' in bcknd:
            bckndarr=readh5pyarray(h5mar['bminbin%d' %getbin(h5analysis)])
        elif 'lin' in bcknd:
            bckndarr, blinwts=readblin(h5mar)
        else:
            bckndarr=readh5pyarray(h5mar['bavebin%d' %getbin(h5analysis)])
        if extrabin>1:
            if 'lin' in bcknd:
                bckndarr=numpy.array([binimage(b, bin=extrabin) for b in bckndarr])
            else:
                bckndarr=binimage(bckndarr, bin=extrabin)
    cb=None
    btuple=None
    if not colorrange is None:
        norm = matplotlib.colors.Normalize(vmin=colorrange[0], vmax=colorrange[1])

    if type==4:
        if 'lin' in bcknd:
            bckndarr=numpy.array([b*killmapbin for b in bckndarr])
        else:
            bckndarr*=killmapbin
        savename1='_'.join((os.path.split(h5path)[1][0:-3], h5groupstr, bcknd[0:3]))
        if datsave:
            if 'lin' in bcknd:
                b0, b1=bckndarr
                b0.tofile(str(''.join((runpath, '/',savename1, '0.dat'))))
                b1.tofile(str(''.join((runpath, '/',savename1, '1.dat'))))
            else:
                bckndarr.tofile(str(''.join((runpath, '/',savename1, '.dat'))))
        else:
            if 'lin' in bcknd:
                for counter, b in enumerate(bckndarr):
                    if not colorrange is None:
                        pyim=pylab.imshow(b, norm=norm)
                    else:
                        pyim=pylab.imshow(b)
                    pylab.savefig(str(''.join((runpath, '/',savename1, `counter`,'.png'))))
                    pylab.cla()
            else:
                if not colorrange is None:
                    pyim=pylab.imshow(bckndarr, norm=norm)
                else:
                    pyim=pylab.imshow(bckndarr)
                pylab.savefig(str(''.join((runpath, '/',savename1, '.png'))))
                pylab.cla()
    else:
        for pointind in pointlist:
            imname=`pointind`
            pnnn=h5mar['countsbin3'][pointind, :, :]
            if extrabin>1:
                pnnn=binimage(pnnn, bin=extrabin)
            if usebanom:
                banom=h5mar['banom'][pointind, :, :]
                btuple=(banom, bminanomf[pointind, 0], bminanomf[pointind, 1])
                #if extrabin>1, banom will get further binned in bckndsubtract()

            if type==0:
                saveim=pnnn
            elif type==1:
                if usebanom:
                    saveim=bckndsubtract(pnnn, bckndarr, killmapbin, btype=bcknd, banom_f_f=btuple)[0]
                elif 'lin' in bcknd:
                    saveim=bckndsubtract(pnnn, bckndarr, killmapbin, btype=bcknd, linweights=blinwts[pointind])[0]
                else:
                    saveim=bckndsubtract(pnnn, bckndarr, killmapbin, btype=bcknd)[0]
            elif type==2:
                saveim=banom
            else:
                saveim=bckndsubtract(pnnn, bckndarr, killmapbin, btype=bcknd, banom_f_f=btuple)[1]

            if datsave:
                saveim.tofile(str(''.join((runpath, '/',savename1, imname, '.dat'))))
            else:
                if not colorrange is None:
                    pyim=pylab.imshow(saveim, norm=norm)
                else:
                    pyim=pylab.imshow(saveim)
                if cb is None:
                    cb = pylab.colorbar()
                else:
                    cb.update_bruteforce(pyim)
                pylab.savefig(str(''.join((runpath, '/',savename1, imname, '.png'))))
                pylab.cla()
    h5file.close()

def plotsoheader(attrdict, xtype):
    sampleline=''.join(('Title/SampleName: ', ''.join(tuple(attrdict['elements']))))
    waveline=''.join(('Wavelength: ',  '%.4f' %attrdict['wavelength'] , 'nm'))
    Lline=''.join(('Detector distance: ',  '%.1f' %attrdict['cal'][2] , 'mm'))
    temp= '\n!@!!'.join(('!@!!XRD integrated',  sampleline,  'Site: Cornell University', waveline, Lline))
    if xtype=='2th':
        temp=''.join((temp, '\n', '!@!XDegrees', '\n!@!YCounts\n'))
    else:
        if xtype=='d':
            temp2='d-spacing (nm)'
        elif xtype=='pix':
            temp2='Detector pixels'
        else:
            temp2='scattering vector (1/nm)'
        temp=''.join((temp, '\n', '!@!!X: ', temp2,'\n!@!YCounts\n'))
    return temp


def readplotso(filename, headerlines=0, splitstr=None):#can use ! in the file or headerlines to skp header
    fin = open(filename, "r")
    lines=fin.readlines()
    fin.close()

    xtype=''
    xvals=[]
    yvals=[]
    for line in lines[headerlines:]:
        if line.startswith('!'):
            if 'XDegrees' in line:
                xtype='2th'
            elif 'X:' in line:
                if 'd-spacing' in line:
                    xtype='d (nm)'
                elif 'pixels' in line:
                    xtype=='pix'
        elif len(line)>2:
            if splitstr is None:
                if '\t' in line:
                    splitstr='\t'
                else:
                    splitstr=' '
            a, b, c=line.partition(splitstr)
            a=a.strip()
            c=c.strip()
            try:
                a=eval(a)
                c=eval(c)
            except:
                continue
            xvals+=[a]
            yvals+=[c]
    if xtype=='':
        xtype='q (1/nm)'
    return numpy.float32(xvals), numpy.float32(yvals), xtype


def calcbanom(h5path,  h5groupstr,  bqgrid=None, bin=3):
#this function for entire pointlist
#if bqgrid is None, use the default bqgrid to calculate bimap or use an already saved bimap. if bqgrid passed then if it is the same as that of saved bimap, use saved bimap, else calc new bimap.
    h5file=h5py.File(h5path, mode='r')
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
    h5mar=h5file['/'.join((h5groupstr, 'analysis', getxrdname(h5analysis)))]

    attrdict=getattr(h5path, h5groupstr)

    pointlist=h5analysis.attrs['pointlist']

    killmap=getkillmap(h5analysis.attrs['killmapstr'], bin=bin)

    imap, qgrid=getimapqgrid(h5analysis.attrs['imapstr'], bin=bin)

    bmin=readh5pyarray(h5mar['bminbin%d' %bin])
    #ALL OF THESE ARE BINNED VERSIONS BUT NAMES AS USUAL
    bminanomf=numpy.ones(h5mar['bminanomf'].shape, dtype='float32')*(-1.0)

    h5file.close()
    killmap*=(imap!=0)

    h5file=h5py.File(h5path, mode='r+')
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
    h5mar=h5file['/'.join((h5groupstr, 'analysis', getxrdname(h5analysis)))]
    h5marcounts=h5file['/'.join((h5groupstr,'measurement', getxrdname(h5analysis), 'counts'))]
    if 'bimap' in h5mar:
        del h5mar['bimap']
    if 'banom' in h5mar:
        del h5mar['banom']
    if 'bminanomf' in h5mar:
        del h5mar['bminanomf']

    banompoint=h5mar.create_dataset('banom', (h5marcounts.shape[0], bmin.shape[0], bmin.shape[1]), dtype='float32')

    z=numpy.zeros((bmin.shape[0], bmin.shape[1]), dtype='float32')
    for pointind in range(banompoint.shape[0]):
        banompoint[pointind, :, :]=z[:, :]

    if 'bimap' in h5mar:
        eval(''.join((fulldergrpstr, '.bimap',  '._f_remove()')))

    bimap=None
    for pointind in pointlist:
        print pointind
        data=h5mar['countsbin%d' %bin][pointind, :, :]
        if bimap is None:
            h5chess=CHESSRUNFILE()
            qimage=readh5pyarray(h5chess[h5analysis.attrs['qimagestr']+'bin%d' %bin])
            h5chess.close()
            cbbf=calc_bmin_banom_factors(data, bmin, killmap, imap, qgrid, attrdict, qimage=qimage)
            bimap=cbbf.bimap
            bqgrid=cbbf.bqgrid
        else:
            cbbf=calc_bmin_banom_factors(data, bmin, killmap, imap, qgrid, attrdict, bimap=bimap, bqgrid=bqgrid)
        bminanomf[pointind, 0]=cbbf.fmin
        bminanomf[pointind, 1]=cbbf.fanom
        banom=cbbf.banom


        totbcknd=(cbbf.fmin*bmin+cbbf.fanom*banom)*killmap
        data*=killmap
        a=data<totbcknd
        bminanomf[pointind, 2]=a.sum()/(1.0*killmap.sum()) #frac pixels zeroed in binned data
        print 'bminanomf:', bminanomf[pointind, :]

        banompoint[pointind, :, :]=banom[:, :]

    print 'banom calculation complete'

    h5mar.create_dataset('bminanomf', data=bminanomf)
    bimappoint=h5mar.create_dataset('bimap', data=bimap)
    bimappoint.attrs['bqgrid']=bqgrid
    updatelog(h5analysis,  ''.join(('banom background calculation for entire pointlist finished ', time.ctime())))
    h5file.close()

def process1dint(h5path, h5groupstr, maxcurv=16.2, type='h5mar:icounts'):
    #makes new solid angle array, deletes and ifnnn and makes a new one for every innn


    h5file=h5py.File(h5path, mode='r+')
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]

    if 'h5mar' in type:
        h5arrname=type.partition(':')[2]
        h5mar=h5file['/'.join((h5groupstr, 'analysis', getxrdname(h5analysis)))]

        if 'ifcounts' in h5mar:
            del h5mar['ifcounts']

        icounts=readh5pyarray(h5mar['icounts'])
        qgrid=h5mar['icounts'].attrs['qgrid']
        pointlist=h5analysis.attrs['pointlist']
        ifcountspoint=h5mar.create_dataset('ifcounts', data=numpy.zeros(icounts.shape, dtype='float32'))
        ifcountspoint.attrs['qgrid']=qgrid
    if 'h5tex' in type:
        h5grpname=type.partition(':')[2]
        h5mar=h5file['/'.join((h5groupstr, 'analysis', getxrdname(h5analysis)))]
        h5tex=h5mar['texture']
        h5texgrp=h5tex[h5grpname]

        if 'ifcounts' in h5texgrp:
            del h5texgrp['ifcounts']

        icounts=readh5pyarray(h5texgrp['icounts'])
        qgrid=h5texgrp.attrs['chigrid']
        pointlist=h5texgrp.attrs['pointlist']
        ifcountspoint=h5texgrp.create_dataset('ifcounts', data=numpy.zeros(icounts.shape, dtype='float32'))
        ifcountspoint.attrs['chigrid']=qgrid


    ifcountspoint.attrs['maxcurv']=maxcurv

    solidangles=None

    for pointind in pointlist:
        print pointind
        ifcountspoint[pointind, :]=bcknd1dprogram(qgrid, icounts[pointind, :], returnall=False, maxcurv=maxcurv)
    #normalization by solidangles removed April 2009. if reinstated, then send attrdictORangle=None for 'h5tex'

    updatelog(h5analysis,  ''.join(('All innn 1D intensity processed. Finished ',  time.ctime())))
    h5file.close()


def wavepeaksearch1d(h5path, h5groupstr, minridgelength=3, minchildlength=0, wavenoisecutoff=2.5, maxqscale_localmax=1.5, minridgewtsum=100., minchildwtsum=0., pointlist=None, verbose=False, type='h5mar'):
    h5file=h5py.File(h5path, mode='r')
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
    h5mar=h5file['/'.join((h5groupstr, 'analysis', getxrdname(h5analysis)))]
    if 'h5mar' in type:
        wtgrpstr='/'.join((h5groupstr, 'analysis', getxrdname(h5analysis), 'wavetrans1d'))
        if pointlist is None:
            pointlist=h5analysis.attrs['pointlist']
    elif 'h5tex' in type:
        h5grpname=type.partition(':')[2]
        h5tex=h5mar['texture']
        h5texgrp=h5tex[h5grpname]
        if pointlist is None:
            pointlist=h5texgrp.attrs['pointlist']
        wtgrpstr='/'.join((h5groupstr, 'analysis', getxrdname(h5analysis), 'texture', h5grpname, 'wavetrans1d'))
    h5file.close()
    errormsg=ridges_wavetrans1d(h5path, wtgrpstr, noiselevel=wavenoisecutoff, pointlist=pointlist)
    if not errormsg is None:
        return errormsg
    errormsg=peaks_ridges1d(h5path, wtgrpstr, minridgelength=minridgelength, minchildlength=minchildlength, maxqscale_localmax=maxqscale_localmax, minridgewtsum=minridgewtsum, minchildwtsum=minchildwtsum, pointlist=pointlist, verbose=verbose)
    if not errormsg is None:
        return errormsg
    h5file=h5py.File(h5path, mode='r+')
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
    h5mar=h5file['/'.join((h5groupstr, 'analysis', getxrdname(h5analysis)))]
    updatelog(h5analysis,  ''.join((type, 'wavelet 1d peak search finished ', time.ctime())))
    h5file.close()

def ridges_wavetrans1d(h5path, h5wtgrpstr, noiselevel=None, numscalesskippedinaridge=1.5, pointlist=None):
    h5file=h5py.File(h5path, mode='r+')
    wtgrp=h5file[h5wtgrpstr]

    qscalegrid=wtgrp.attrs['qscalegrid']
    qscalevals=scale_scalegrid_ind(qscalegrid)
    qposngrid=wtgrp.attrs['qposngrid']
    qposnint=qposngrid[1]

    qsindlist=[2*max(int(numpy.ceil(1.*qs/qposnint)), 1) for qs in qscalevals[::-1]]

    wtpoint=wtgrp['wavetrans']

    nonoisecut=(noiselevel is None)
    ridges_pointlist=[]

    for pointind in pointlist:
        temp=wtpoint[pointind, :, :]#reverse first index so that it goes from widest to smallest scale
        wtrev=temp[::-1, :]
        if nonoisecut:
            noiselevel=wtrev.min()
        ridges_pointlist+=[perform_ridges_wavetrans1d(wtrev, qsindlist, noiselevel, numscalesskippedinaridge=numscalesskippedinaridge)]

    numr_pointlist=[len(r) for r in ridges_pointlist]
    maxnr=max(numr_pointlist)
    filler=[[32767]*wtrev.shape[0]]*maxnr
    for r in ridges_pointlist:
        r+=filler[:len(filler)-len(r)]
    ridgessav=32767*numpy.ones((wtpoint.shape[0], maxnr, wtrev.shape[0]), dtype='int16')
    ridgessav[numpy.array(pointlist), :, :]=numpy.int16(ridges_pointlist)
    if 'ridges' in wtgrp:
        del wtgrp['ridges']
    wtgrp.create_dataset('ridges', data=ridgessav)
    wtgrp.attrs['noiselevel']=noiselevel
    wtgrp.attrs['numscalesskippedinaridge']=numscalesskippedinaridge
    h5file.close()

def peaks_ridges1d(h5path, h5wtgrpstr, minridgelength=3, minchildlength=0., maxqscale_localmax=1.5, minridgewtsum=100., minchildwtsum=0., pointlist=[], verbose=False): #the qwidthrange is in /nm and the ridge must have a local maximum in that range

    minridgelength=max(1, minridgelength)
    h5file=h5py.File(h5path, mode='r+')
    wtgrp=h5file[h5wtgrpstr]

    qscalegrid=wtgrp.attrs['qscalegrid']
    ridgeqscalevals=scale_scalegrid_ind(qscalegrid)[::-1] #ordered big->small

    ridgescalecritind=numpy.where(ridgeqscalevals<=maxqscale_localmax)[0]
    if len(ridgescalecritind)<2:
        h5file.close()
        print 'aborted: the set of qscales does not include more than 1 point in the specified qwidthrange'
        return 'aborted: the set of qscales does not include more than 1 point in the specified qwidthrange'
    ridgescalecritind=ridgescalecritind[0] #takes the last because these are in decreasing order now

    wtpoint=wtgrp['wavetrans']
    ridgespoint=wtgrp['ridges']
    peaks_pointlist=[]

    for pointind in pointlist:
        wt=wtpoint[pointind, :, :]
        ridges=ridgespoint[pointind, :, :]

        peaks_pointlist+=[perform_peaks_ridges1d(wt, ridges, ridgescalecritind=ridgescalecritind, minridgelength=minridgelength, minchildlength=minchildlength, minridgewtsum=minridgewtsum, minchildwtsum=minchildwtsum, verbose=verbose)]
    #print 'peaks:', peaks_pointlist
    #h5file.close()
    #return

    numpks_pointlist=[len(p) for p in peaks_pointlist]
    maxnp=max(numpks_pointlist)
    filler=[[32767]*2]*maxnp
    for p in peaks_pointlist:
        p+=filler[:len(filler)-len(p)]
    peakssav=numpy.ones((wtpoint.shape[0], 2, maxnp), dtype='uint16')*32767
    def pksort(arr):
        sortind=arr[1].argsort()
        return numpy.uint16([arr[0, sortind], arr[1, sortind]])
    peakssav[numpy.array(pointlist), :, :]=numpy.uint16([pksort(numpy.uint16(p).T) for p in peaks_pointlist])
    if 'peaks' in wtgrp:
        del wtgrp['peaks']
    wtgrp.create_dataset('peaks', data=peakssav)
    wtgrp.attrs['minridgelength']=minridgelength
    wtgrp.attrs['maxqscale_localmax']=maxqscale_localmax
    wtgrp.attrs['minridgewtsum']=minridgewtsum
    wtgrp.attrs['minchildlength']=minchildlength
    wtgrp.attrs['minchildwtsum']=minchildwtsum
    h5file.close()

def getchiminmax(chessh5grpstr):
    h5chess=CHESSRUNFILE()
    h5grp=h5chess[chessh5grpstr]
    cal=h5grp.attrs['cal']
    alpharad=h5grp.attrs['alpha']*numpy.pi/180
    L=cal[2]
    wl=h5grp.attrs['wavelength']
    qvals=set([])
    for dset in h5grp['imap'].iterobjects():
        if isinstance(dset, h5py.Dataset) and ('qgrid' in dset.attrs):
            qgrid=dset.attrs['qgrid']
            qvals|=set(q_qgrid_ind(qgrid))
    h5chess.close()
    if len(qvals)==0:
        print 'no imaps found to help with chimap range'
        return (0, 1)

    chivals=numpy.array([[chi_q_azim(q, azim, alpharad, L, wl) for q in qvals] for azim in [0, numpy.pi/2.0, numpy.pi, 1.5*numpy.pi]])*180.0/numpy.pi
    return (numpy.min(chivals), numpy.max(chivals)) #try obvious combinations of q and azim to find the max and min chivals so that this algorithm is robusts to simple changes in experiment geometry

def readsampleinfotxt(filename):
    fin = open(filename, "r")
    lines=fin.readlines()
    fin.close()
    headings=[]
    vals=[]
    for line in lines:
        temp=line
        if line[0].isalpha():
            while len(temp.partition('\t')[2])>0:
                temp2,  garbage, temp=temp.partition('\t')
                headings+=[temp2]
            headings+=[temp.partition('\n')[0]]
        else:
            rowvals=[]
            while len(temp.partition('\t')[2])>0:
                temp2,  garbage, temp=temp.partition('\t')
                rowvals+=[temp2]
            rowvals+=[temp.partition('\n')[0]]
            vals+=[rowvals]
    vals=numpy.float32(vals).T
    headings.pop(0)

    return headings,  list(numpy.uint16(numpy.round(vals[0]))), vals[1:]

def importsampleinfotoh5(h5path, h5groupstr, importfilepath):#zeroth column of arr MUST be spec imagenumber
    head, pointinds, vals=readsampleinfotxt(importfilepath)
    h5file=h5py.File(h5path, mode='r+')
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
    if 'otherdata' in h5analysis:
        h5otherdata=h5analysis['otherdata']
    else:
        h5otherdata=h5analysis.create_group('otherdata')
    attrdict=getattr(h5path, h5groupstr)
    numpts=numpts_attrdict(attrdict)
    info=numpy.empty(numpts, dtype='float32')
    for nam, arr in zip(head, vals):
        info=numpy.ones(numpts, dtype='float32')*numpy.nan
        for ind, v in zip(pointinds, arr):
            info[ind]=v
        if nam in h5otherdata:
            del h5otherdata[nam]
        h5otherdata.create_dataset(nam, data=info)

    print "'Other Data' arrays created for ", ', '.join(head)
    h5file.close()

def getpointinfo(h5path, h5groupstr, types=[]):#returns several types of info for each spec point. In addition to x,z substrate coordinates there are deposition profile (DP), XRF and OTHER types of data - all arrays indexed by spec index and become dictionary entries. Some 'types' get several arrays,e.g. mol fractions. boolean 'success' let's you know if all the requested types were found.


    attrdict=getattr(h5path, h5groupstr)
    numpts=numpts_attrdict(attrdict)
    h5file=h5py.File(h5path, mode='r')
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]

    if 'depprof' in h5analysis:
        h5depprof=h5analysis['depprof']
        gunpropdict=ReadGunPropDict(h5analysis)
    if 'xrf' in h5analysis:
        h5xrf=h5analysis['xrf']
    if 'otherdata' in h5analysis:
        h5otherdata=h5analysis['otherdata']
    alltypes=['x(mm)', 'z(mm)', 'DPnmolscm2ALL', 'DPmolfracALL', 'DPmassfracALL', 'DPgcm3', 'DPnmolcm2', 'DPnm', 'XRFmolfracALL', 'XRFnm', 'XRFareaALL', 'XRFsigareaALL', 'OTHER']
    if types==[]:
        types=alltypes
    else:
        types=[ty for ty in types if ty in alltypes]
    d={}
    success=True
    for ty in types:
        try:
            if ty.startswith('DP'):
                if 'ALL' in ty:
                    temp=ty.partition('DP')[2].partition('ALL')[0]
                    for i, el in zip(gunpropdict['guninds'], gunpropdict['symbol']):
                        d['DP%s_%s' %(temp, el)]=readh5pyarray(h5depprof['%sgun%d' %(temp, i)])
                else:
                    temp=ty.partition('DP')[2]
                    d[ty]=readh5pyarray(h5depprof[temp])

            elif ty.startswith('XRF'):
                if 'ALL' in ty:
                    if 'area' in ty:
                        for dset in h5xrf['areas'].iterobjects():
                            if isinstance(dset, h5py.Dataset):
                                temp=ty.partition('ALL')[0]
                                d['%s_%s' %(temp, dset.name.rpartition('/')[2])]=readh5pyarray(dset)[:, 'sig' in ty]
                    else:
                        temp=ty.partition('XRF')[2].partition('ALL')[0]
                        for el, arr in zip(h5xrf.attrs['elements'], readh5pyarray(h5xrf[temp]).T):
                            d['XRF%s_%s' %(temp, el)]=arr
                else:
                    temp=ty.partition('XRF')[2]
                    d[ty]=readh5pyarray(h5xrf[temp])

            elif ty.startswith('OTHER'):
                for dset in h5otherdata.iterobjects():
                        if isinstance(dset, h5py.Dataset) and len(dset.shape)==1 and dset.shape[0]==numpts:
                            d['OTHER_%s' %dset.name.rpartition('/')[2]]=readh5pyarray(dset)
            elif  ty=='x(mm)' or ty=='z(mm)':
                d['x(mm)']=attrdict['x']
                d['z(mm)']=attrdict['z']
            else:
                print 'WARNING: pointinfo type ', ty, ' not understood'
                success=False
        except: #if the data doesn't exist then skip and go on
            print 'WARNING: ', ty, 'not found'
            success=False
            continue

    h5file.close()
    return d, success

def pointinfodictkeysort(d):
    def metric(k):
        v=1
        if k=='x(mm)':
            return 10000
        if k=='z(mm)':
            return 10001
        v*=(1+999*('DP' in k))
        v*=(1+99*(('XRF' in k) and not ('area' in k)))
        v*=(1+9*('OTH' in k))
        v+=(('XRF' in k) and ('area' in k) and not ('sig' in k))
        v+='molfrac' in k
        return v
    kv=[[k, metric(k)] for k in d.keys()]
    kv.sort(key=operator.itemgetter(1), reverse=True)
    return [k[0] for k in kv]

def binmapsinh5chess(chessh5grpstr, bin=3):
        h5chess=CHESSRUNFILE('r+')
        h5grp=h5chess[chessh5grpstr]
        print chessh5grpstr, h5grp.listitems()
        grps=[h5grp['imap'], h5grp['chimap'], h5grp['killmap']]
        cmdstr=['binimage(arr, bin=bin, zerokill=True)', 'binimage(arr, bin=bin, zerokill=True)', 'binboolimage(arr, bin=bin)']
        for grp, cs in zip(grps, cmdstr):
            for dset in grp.iterobjects():
                if isinstance(dset, h5py.Dataset) and not ('bin' in dset.name):
                    binname=dset.name+('bin%d' %bin)
                    if not (binname in grp):
                        arr=readh5pyarray(dset)
                        h5grp.create_dataset(binname, data=eval(cs))

        h5chess.close()

def buildwaveset1d(qscalegrid, qposngrid, qgrid, maxfixenfrac=0.12, enfractol=0.0, maxoverenergy=None):
    ENERGY=0.57457 #this is constant fro all scales and translations
    maxfixenfrac+=1 #this notes a discrepancy between fixenfrac in GUI and in code and saved attribute
    if maxoverenergy is None:
        maxoverenergy=maxfixenfrac
    waveattrdict={'qgrid':qgrid, 'qscalegrid':qscalegrid, 'qposngrid':qposngrid,'ENERGY':ENERGY, 'maxfixenfrac':maxfixenfrac, 'maxoverenergy':maxoverenergy, 'enfractol':enfractol}

    dq=qgrid[1]
    waveset=waveletset1d(qgrid, qscalegrid, qposngrid)
    a, b, c=waveset.shape
    fixenarr=numpy.empty((a, b), dtype='float32')
    for i in range(a):
        for j in range(b):
            en=((waveset[i, j, :]**2)*dq).sum()
            fixenfrac=ENERGY/en
            if fixenfrac<maxfixenfrac and 1/fixenfrac<maxoverenergy:
                if en<((1.0-enfractol)*ENERGY) or en>((1.0+enfractol)*ENERGY):
                    waveset[i, j, :]=wave1dkillfix(waveset[i, j, :], ENERGY, dq=dq)*dq
                else:
                    fixenfrac=0.0
                    waveset[i, j, :]*=dq
                fixenarr[i, j]=fixenfrac
            else:
                waveset[i, j, :]*=numpy.nan
                fixenarr[i, j]=numpy.nan

    if numpy.isnan(fixenarr).sum()==fixenarr.size:
        print 'every wavelet calculation resulted in error. check energy. nothing saved'
        return


    h5wave=WAVESET1dFILE('r+')
    grpname='_'.join([','.join([labelnumberformat(num) for num in qscalegrid]), ','.join([labelnumberformat(num) for num in qposngrid]), ','.join([labelnumberformat(num) for num in qgrid])])
    if grpname in h5wave:
        del h5wave[grpname]
    wavegrp=h5wave.create_group(grpname)
    for key, val in waveattrdict.iteritems(): #because h5py doesn't have bools - this can be removed when new version of h5py arrives
        if isinstance(val, bool):
            wavegrp.attrs[key]=int(val)
        else:
            wavegrp.attrs[key]=val

    wavegrp.create_dataset('waveset', data=waveset)
    wavegrp.create_dataset('fixenfrac', data=fixenarr)

    h5wave.close()

def wavetrans1d(h5path, h5groupstr, wavesetname, type='h5mar:icounts'):#wavetrans qgrid can be subset of icounts qgrid but not vice versa
#    print "h5path='", h5path, "'"
#    print "h5groupstr='", h5groupstr, "'"
#    print "wavesetname='", wavesetname, "'"
    h5wave=WAVESET1dFILE()

    wavegrp=h5wave[wavesetname]
    waveset=wavegrp['waveset'][:, :, :]
    waveqgrid=wavegrp.attrs['qgrid']

    h5file=h5py.File(h5path, mode='r+')
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]

    if 'h5mar' in type:
        h5arrname=type.partition(':')[2]
        h5mar=h5file['/'.join((h5groupstr, 'analysis', getxrdname(h5analysis)))]

        if 'wavetrans1d' in h5mar:
            del h5mar['wavetrans1d']
        wtgrp=h5mar.create_group('wavetrans1d')
        icountspoint=h5mar[h5arrname]
        qgrid=icountspoint.attrs['qgrid']
    if 'h5tex' in type:
        h5grpname=type.partition(':')[2]
        h5mar=h5file['/'.join((h5groupstr, 'analysis', getxrdname(h5analysis)))]
        h5tex=h5mar['texture']
        h5texgrp=h5tex[h5grpname]

        if 'wavetrans1d' in h5texgrp:
            del h5texgrp['wavetrans1d']
        wtgrp=h5texgrp.create_group('wavetrans1d')
        icountspoint=h5texgrp['icounts']
        qgrid=h5texgrp.attrs['chigrid']

    wtgrp.attrs['wavesetname']=wavesetname
    qscalegrid=wavegrp.attrs['qscalegrid']
    for key, val in wavegrp.attrs.iteritems():
        wtgrp.attrs[key]=val
    wtgrp.create_dataset('fixenfrac', data=wavegrp['fixenfrac'][:, :])
    h5wave.close()

    pointlist=h5analysis.attrs['pointlist']


    a, b, c =waveset.shape # num scales, num posn, length of data
    dfltarr=numpy.empty((a, b), dtype='float32')*numpy.nan


    icind=numpy.array([qval in q_qgrid_ind(waveqgrid) for qval in q_qgrid_ind(qgrid)])

    wt=wtgrp.create_dataset('wavetrans', (icountspoint.shape[0], a, b))
    #for ind in set(range(wt.shape[0]))-set(pointlist):
    for ind in range(wt.shape[0]):
        wt[ind, :, :]=dfltarr[:, :]
    for pointind in pointlist:
        data=icountspoint[pointind][icind]
        datainds=numpy.where(numpy.logical_not(numpy.isnan(data))) # this violates the philosophy that the wavelets should be correected before hand - active wavelet stretching could be added here
        #wt[pointind, :, :]=numpy.float32([[(vec*data).sum() for vec in arr] for arr in waveset])
        print '*', pointind, data.shape, waveset.shape, scale_scalegrid_ind(qscalegrid).shape
        wt[pointind, :, :]=numpy.float32([[(vec*data)[datainds].sum()/scale for vec in arr] for arr, scale in zip(waveset, scale_scalegrid_ind(qscalegrid))])
    h5file.close()

def peakfit1d(h5path, h5groupstr, windowextend_hwhm=3, peakshape='Gaussian', critresidual=.2, use_added_peaks=False, type='h5mar'):
    try:
        peakfcn=eval(peakshape)
    except:
        print 'ABORTED: did not understand peak shape "',peakshape,'" - this must be an already defined function.'
        return 'ABORTED: did not understand peak shape "',peakshape,'" - this must be an already defined function.'

    h5file=h5py.File(h5path, mode='r')
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
    h5mar=h5file['/'.join((h5groupstr, 'analysis', getxrdname(h5analysis)))]
    if 'h5mar' in type:
        wtgrpstr='/'.join((h5groupstr, 'analysis', getxrdname(h5analysis), 'wavetrans1d'))
        pointlist=h5analysis.attrs['pointlist']
        ifcountspoint=h5mar['ifcounts']
        numpts=ifcountspoint.shape[0]
        qgrid=h5mar['ifcounts'].attrs['qgrid']
        h5grpstr='/'.join((h5groupstr, 'analysis', getxrdname(h5analysis)))

    elif 'h5tex' in type:
        h5grpname=type.partition(':')[2]
        h5tex=h5mar['texture']
        h5texgrp=h5tex[h5grpname]
        pointlist=h5texgrp.attrs['pointlist']
        wtgrpstr='/'.join((h5groupstr, 'analysis', getxrdname(h5analysis), 'texture', h5grpname, 'wavetrans1d'))
        h5grpstr='/'.join((h5groupstr, 'analysis', getxrdname(h5analysis), 'texture', h5grpname))
        ifcountspoint=h5texgrp['ifcounts']
        numpts=ifcountspoint.shape[0]
        qgrid=h5texgrp['ifcounts'].attrs['chigrid']



    wtgrp=h5file[wtgrpstr]

    qvals=q_qgrid_ind(qgrid)

    qscalegrid=wtgrp.attrs['qscalegrid']
    qposngrid=wtgrp.attrs['qposngrid']

    wtpeakspoint=wtgrp['peaks']

    if 'additionalpeaks' in h5file[h5grpstr] and use_added_peaks:
        addpeaks=readh5pyarray(h5file[h5grpstr]['additionalpeaks'])
    else:
        addpeaks=None

    #pointlist=[41, 49]#***
    qshsss=[] #q values, scale value, height, sigma q scale, sigma sclae, sigma height
    for peakind in pointlist:
        #print 'point', peakind
        counts=ifcountspoint[peakind]
        notnaninds=numpy.where(numpy.logical_not(numpy.isnan(counts)))[0]
        wtpeakdata=wtpeakspoint[peakind, :, :]
        qscales=wtpeakdata[0, :]
        qposns=wtpeakdata[1, :]
        qscales=qscales[qscales!=32767]
        qposns=qposns[qposns!=32767]
        qscales=scale_scalegrid_ind(qscalegrid, qscales)
        #print qscales
        qscales*=0.36 #for wavelet->Gaussian HWHM
        qposns=q_qgrid_ind(qposngrid, qposns)
        if not (addpeaks is None):
            addpeakinds=numpy.where(numpy.uint16(numpy.round(addpeaks[:, 0]))==peakind)
            if len(addpeakinds[0])>0:
                #print addpeaks[addpeakinds, 1], '**',addpeaks[addpeakinds, 2]
                qscales=numpy.append(qscales, addpeaks[addpeakinds, 1])
                qposns=numpy.append(qposns, addpeaks[addpeakinds, 2])
                sortinds=qposns.argsort()
                qposns=qposns[sortinds]
                qscales=qscales[sortinds]
                #print qposns
                #print qscales
        if len(qscales)==0:
            qshsss+=[numpy.float32([[]])]
            continue
        qscales=numpy.float32([max(qs, .25) for qs in qscales])#this is intended for overlapping peaks where wt will give very low qscale.
        indrangeandpeakinds=windows_peakpositions(qgrid, qscales, qposns, windowextend_qscales=windowextend_hwhm)
        #print 'windows', indrangeandpeakinds
        pars=None
        sigs=None
        for indrange, peakinds in indrangeandpeakinds:
            startpars=[[qposns[i], qscales[i], counts[notnaninds[numpy.argmin((notnaninds-ind_qgrid_q(qgrid, qposns[i]))**2)]]] for i in peakinds]
            #print 'startpars',  startpars
            inds=list(set(notnaninds)&set(range(indrange[0], indrange[1])))
            if len(inds)==0:
                print 'THIS WILL CRASH BECUASE THERE ARE NO VALID DATA POINT IN THIS WINDOW - THE DATA INDEX ENDPOINTS BEFORE NANs WERE REMOVED WERE ' , indrange[0], indrange[1]
            p, s, r=fitpeakset(qvals[inds], counts[inds], startpars, peakfcn)
            if pars is None:
                pars=p[:, :]
                sigs=s[:, :]
            else:
                pars=numpy.concatenate((pars,p),axis=0)
                sigs=numpy.concatenate((sigs,s),axis=0)
        qshsss+=[numpy.concatenate((pars.T,sigs.T),axis=0)]
    h5file.close()
    #print qshsss
    #return
    maxnumpeaks=max([arr.shape[1] for arr in qshsss])
    savearr=numpy.ones((numpts, 6, maxnumpeaks), dtype='float32')*numpy.nan
    for pointind, arr in zip(pointlist, qshsss):
        savearr[pointind, :, :arr.shape[1]]=arr[:, :]

    h5file=h5py.File(h5path, mode='r+')
    h5grp=h5file[h5grpstr]
    if 'pkcounts' in h5grp:
        del h5grp['pkcounts']
    pkcounts=h5grp.create_dataset('pkcounts', data=savearr)
    pkcounts.attrs['windowextend_hwhm']=windowextend_hwhm
    pkcounts.attrs['peakshape']=peakshape
    pkcounts.attrs['critresidual']=critresidual

    if not (addpeaks is None):
        h5grp['additionalpeaks'].attrs['usedinfitting']=1
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
    updatelog(h5analysis,  ''.join((type, ' peak fitting. ', time.ctime())))
    h5file.close()


def getpeaksinrange(h5path, h5groupstr, indlist=None, qmin=0, qmax=1000, returnonlyq=True,  performprint=False, returnonlytallest=True):
    h5file=h5py.File(h5path, mode='r')
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
    h5mar=h5file['/'.join((h5groupstr, 'analysis', getxrdname(h5analysis)))]

    pkcounts=readh5pyarray(h5mar['pkcounts'])
    pointlist=h5analysis.attrs['pointlist']
    returnpointinds=[]
    returnpeakinfo=[]
    if indlist is None:
        indlist=pointlist
    for i in indlist:
        a, b, c, d, e, f=peakinfo_pksavearr(pkcounts[i,:,:], fiterr=True)
        goodinds=numpy.where((a>=qmin)&(a<=qmax))
        if len(goodinds[0])>0:
            if returnonlytallest:
                printindlist=[goodinds[0][myargmax(c[goodinds])]]
            else:
                printindlist=goodinds[0]
            for printind in printindlist:
                returnpointinds+=[i]
                if returnonlyq:
                    returnpeakinfo+=[a[printind]]
                    if performprint:
                        print i, '\t', a[printind]
                else:
                    returnpeakinfo+=[[a[printind], b[printind], c[printind], d[printind], e[printind], f[printind]]]
                    if performprint:
                        print '\t'.join((`i`, `a[printind]`, `b[printind]`, `c[printind]`, `d[printind]`, `e[printind]`, `f[printind]`))
            continue
        if performprint:
            print '\t'*6*(1-returnonlyq)
    h5file.close()
    return returnpointinds, numpy.float32(returnpeakinfo) #if indlist had no peaks then it is not in returnointlist

def writedepprof(h5path, h5groupstr, gunpropdict, mappedquantdict):
    h5file=h5py.File(h5path, mode='r+')
    #node=h5file[h5groupstr]
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
    if 'depprof' in h5analysis:
        del h5analysis['depprof']
    h5depprof=h5analysis.create_group('depprof')
    for key, val in gunpropdict.iteritems():
        if isinstance(val, list) and len(val)==0:
            continue
        h5depprof.attrs[key]=val
    for key, val in mappedquantdict.iteritems():
        print key, type(val)
        if isinstance(val, numpy.ndarray):
            if key in h5depprof:
                del h5depprof[key]
            h5depprof.create_dataset(key, data=val)
    h5file.close()

def get_elMd_el(ellist): #ellist should be a list of element symbols. If el is not recognized it will not be in the return list
    #elsymbols=[Elemental.table[i].symbol for i in range(len(Elemental.table))] #could alternatively use PyMEl.ElementsInfo which is alist of the elements. for each element there is a list where symbol, M, d*1000 are at indeces 0, 5, 6
    smd=[[l[0],l[5],l[6]/1000.] for l in PyMEl.ElementsInfo]
    elsymbols=map(operator.itemgetter(0),smd)
    elmass=map(operator.itemgetter(1),smd)
    eldens=map(operator.itemgetter(2),smd)

    temp=[[el, elsymbols.index(el)] for el in ellist if el in elsymbols] #is element info was not provided then it will be looked up in the below lines. but if the element symbol is not found it will be excluded from analysis

    if len(temp)==0:
        print 'ABORTING: could not find info on any of the elements'
        return None
    if len(temp)<len(ellist):
        print 'SOME ELEMENTS NOT RECOGNIZED - THEY WERE SKIPPED'
    #return [[el, Elemental.table[elind].atomic_mass.value, Elemental.table[elind].density_solid.value] for el, elind in temp]
    return [[el, elmass[elind], eldens[elind]] for el, elind in temp]

def getinfoforxrf(h5path, h5groupstr):#***
    h5file=h5py.File(h5path, mode='r')
    #node=h5file[h5groupstr]
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
    gunpropdict=ReadGunPropDict(h5analysis)
    if gunpropdict is None:
        gunpropdict={}
        gunpropdict['symbol']=getattr(h5path, h5groupstr)['elements']
        if not (set(['CenterMolRates', 'M', 'd'])<=set(gunpropdict.keys())):

            temp=get_elMd_el(gunpropdict['symbol'])
            if temp is None:
                elsym, elM, eld=([], [], [])
            else:
                elsym, elM, eld = zip(*temp)

            gunpropdict['symbol']=list(elsym)
            gunpropdict['M']=list(elM)
            gunpropdict['d']=list(eld)
            gunpropdict['CenterMolRates']=[2.]*len(elsym)#default to 2nmol/s/cm2 for every element
            return gunpropdict, None, None
    h5depprof=h5analysis['depprof']

    comp=[]
    for i in range(4):
        s='molfracgun%d' %i
        if s in h5depprof:
            comp+=[readh5pyarray(h5depprof[s])]
    comp=numpy.float32(comp).T
    nm=readh5pyarray(h5depprof['nm'])
    h5file.close()
    return gunpropdict, comp, nm

#def XRFanalysis(h5path, h5groupstr, elements, BckndCounts, FluxCal, DepProfEst, Underlayer, Sicm,  SecondaryAction='Notify', ICcts='IC3', cfgpath=None):
def XRFanalysis(h5path, h5groupstr, elements, quantElTr, eld, elM, approxstoich, BckndCounts, RepEn, cfgpath,  otherElTr, FluxCal, DepProfEst,  Underlayer, Sicm, time, dlambda='', mflambda='', SecondaryAction='Notify'):

    attrdict=getattr(h5path, h5groupstr)
    pointlist=attrdict['pointlist']

    infoforxrf=getinfoforxrf(h5path, h5groupstr)

    h5file=h5py.File(h5path, mode='r')
    h5mcacountspoint=h5file['/'.join((h5groupstr, 'measurement/MCA/counts'))]
    counts=readh5pyarray(h5mcacountspoint)
    timearr=readh5pyarray(h5file['/'.join((h5groupstr, 'measurement/scalar_data', time))])
    h5file.close()

    be=eV_nm(attrdict['wavelength'])/1000.0

    #pointlist=numpy.array([112])

    est_film_comp=approxstoich
    est_film_nm = 100.0
    if isinstance(FluxCal, float):
        flux=FluxCal
        pointind_fluxcal=None
    elif isinstance(FluxCal, str) and FluxCal.startswith("CalUsing"):
        if infoforxrf[2] is None or set(elements)!=set(infoforxrf[0]):
            print 'ABORTING: '+FluxCal+' requested but the DepProf data is not available.'
            return 'ABORTING: '+FluxCal+' requested but the DepProf data is not available.'
        flux=None
        pointind_fluxcal=eval(FluxCal.partition("CalUsing")[2])
        est_film_nm = infoforxrf[2][pointind_fluxcal]
    else:
        pointind_fluxcal=None
        flux=None

    if DepProfEst:
        if infoforxrf[1] is None:
            print 'ABORTING: DepProf estimates for film comp and thickness were requested but the DepProf data is not available.'
            return 'ABORTING: DepProf estimates for film comp and thickness were requested but the DepProf data is not available.'
        est_film_comp = infoforxrf[1][pointlist]
        est_film_nm = infoforxrf[2][pointlist]

    global d#even though eld and elM are passed to XRFanalyzer, any global variables used in the lambda functions must be defined here
    global M #these get deleted at the end
    d=numpy.float32(eld)
    M=numpy.float32(elM)

    lambdafcns=[None, None]
    lambdastrlist=[dlambda, mflambda]
    testcomp=numpy.ones(len(quantElTr), dtype='float32')/len(quantElTr)
    for count, lstr in enumerate(lambdastrlist):
        if lstr!='':
            try:
                if 'i' in lstr:
                    f=eval(lstr)
                    lambdafcns[count]=[f(i) for i in pointlist]
                    justfortest=[f(testcomp) for f in lambdafcns[count]]
                else:
                    lambdafcns[count]=eval(lstr)
                    justfortest=lambdafcns[count](testcomp)
            except:
                del d
                del M
                print 'ABORTING XRF CALCULATION: problem with ', (count==0 and 'density') or 'massfrac', ' lambda function'
                return 'ABORTING XRF CALCULATION: problem with ', (count==0 and 'density') or 'massfrac', ' lambda function'


    xrfan=XRFanalyzer(counts, elements, quantElTr, eld, elM, BckndCounts=BckndCounts, RepEn=RepEn, cfgpath=cfgpath,  otherElTr=otherElTr, pointlist=list(pointlist), beamenergy=be, est_film_comp=est_film_comp, est_film_nm = est_film_nm, SecondaryAction=SecondaryAction, Sicm=Sicm, Underlayer_El_d_nm=Underlayer, pointind_fluxcal=pointind_fluxcal, flux=flux, daqtime=timearr, densfcn=lambdafcns[0], mffcn=lambdafcns[1])

    h5file=h5py.File(h5path, mode='r+')
    h5node=h5file['/'.join((h5groupstr, 'analysis'))]


    if 'xrf' in h5node:
        del h5node['xrf']
    h5xrf=h5node.create_group('xrf')
    if 'areas' in h5xrf:
        del h5xrf['areas']
    h5xrfareas=h5xrf.create_group('areas')


    h5xrf.attrs['elements']=elements
    h5xrf.attrs['quantElTr']=quantElTr
    h5xrf.attrs['d']=d
    h5xrf.attrs['M']=M
    h5xrf.attrs['BckndCounts']=BckndCounts
    h5xrf.attrs['RepEn']=RepEn
    h5xrf.attrs['dlambda']=dlambda
    h5xrf.attrs['mflambda']=mflambda
    h5xrf.create_dataset('molfrac', data=xrfan.comp_res)
    h5xrf.create_dataset('nm', data=xrfan.thick_res)
    h5xrf.create_dataset('cfg', data=numpy.array(xrfan.cfgstr))

    pks=xrfan.resultdict[pointlist[0]].keys()
    pks=[(p, p.replace(' ',''), numpy.zeros((counts.shape[0], 2), dtype='float32')) for p in pks]
    for k, nam, arr in pks:
        for ind in pointlist:
            arr[ind, 0]=xrfan.resultdict[ind][k]['fitarea']
            arr[ind, 1]=xrfan.resultdict[ind][k]['sigmaarea']
        h5xrfareas.create_dataset(nam, data=arr)

    h5file.close()
    if True: #to make this a different code block
        del d
        del M

def elements_elstr(elstr, min_num_els=3):
    elstrlist=[]
    inds=[]
    for count, ch in enumerate(elstr):
        if ch.isupper():
            inds+=[count]
    inds+=[count+1]
    for i, j in zip(inds[:-1], inds[1:]):
        elstrlist+=[elstr[i:j]]
    if len(elstrlist)<min_num_els:
        elstrlist+=['X']*(min_num_els-len(elstrlist))
    el_gun=[]
    for count, el in enumerate(elstrlist):
        if el!='X':
            el_gun+=[[el, count]]
    return elstrlist, el_gun
#def elements_elstr(elstr, min_num_els=3): #from Nov 2010 but reverted to above June2010 which may have worked better??
#    if isinstance(elstr, str):
#        elstrlist=[]
#        inds=[]
#        for count, ch in enumerate(elstr):
#            if ch.isupper():
#                inds+=[count]
#        inds+=[count+1]
#        for i, j in zip(inds[:-1], inds[1:]):
#            elstrlist+=[elstr[i:j]]
#        if len(elstrlist)<min_num_els:
#            elstrlist+=['X']*(min_num_els-len(elstrlist))
#        el_gun=[]
#        for count, el in enumerate(elstrlist):
#            if el!='X':
#                el_gun+=[[el, count]]
#    else:
#        elstr=numpy.array(elstr)
#        ginds=numpy.where(numpy.logical_and(elstr!='X', elstr!=''))
#        if len(ginds[0])<min_num_els:
#            elstr[elstr=='']='X'
#            elstrlist=list(elstr)+['X']*(min_num_els-len(elstr))
#        else:
#            elstrlist=list(elstr[ginds])
#        el_gun=[[e, g] for e, g in zip(elstr[ginds], ginds[0])]
#    return elstrlist, el_gun

def getcomps(h5path, h5groupstr, elstrlist=None, infotype='DPmolfracALL', normalize=True, num_els=None): #elstrlist is a list of elments symbols or 'X' or whatever and comlist should be a 'type' of getpointinfo with 'ALL',  if an element is not found in the data then its composition will be zero. If elstrlist is passed, num_els is ignored, otherwise the array is guarenteed to have num_else compositions that are normalized where possible
    if elstrlist is None:
        h5file=h5py.File(h5path, mode='r')
        h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
        if 'depprof' in h5analysis: #even if getting XRF data, use the element list from dep profiles if possible
            elstrlist=list(h5analysis['depprof'].attrs['symbol'])
            if not num_els is None:
                if len(elstrlist)>=num_els:
                    elstrlist=elstrlist[:num_els]
                else:# not enough elements so make a list of elements, filling in the ones we have in the appropriate gunind spots
                    guninds=h5analysis['depprof'].attrs['guninds'][:]
                    temp=copy.copy(elstrlist)
                    elstrlist=[]
                    for i in range(num_els):
                        if i in guninds:
                            elstrlist+=[temp[numpy.where(guninds==i)[0]]]
                        else:
                            elstrlist+=['X']
        elif 'xrf' in h5analysis:
            elstrlist=list(h5analysis['xrf'].attrs['elements'])
            if not num_els is None:
                if len(elstrlist)>=num_els:
                    elstrlist=elstrlist[:num_els]
                else:
                    elstrlist+=['X']*(num_els-len(elstrlist))
        h5file.close()
    infodict, success=getpointinfo(h5path, h5groupstr, types=[infotype])
    if not success:
        return None, None
    keyroot=infotype.partition('ALL')[0]
    foundkeys=[(count, keyroot+'_'+el) for count, el in enumerate(elstrlist) if keyroot+'_'+el in infodict.keys()]
    if len(foundkeys)==0:
        return None, None
    comps=numpy.zeros((len(infodict[foundkeys[0][1]]), len(elstrlist)), dtype='float32')
    for (ind, k) in foundkeys:
        comps[:, ind]=infodict[k][:]
    if normalize:
        tot=comps.sum(axis=1)
        tot[tot==0.]=1.
        comps=numpy.float32([c/t for c, t in zip(comps, tot)])
    return elstrlist, comps


def getternarycomps(h5path, h5groupstr, elstr=None, infotype='DPmolfracALL'):
        if elstr is None:
            compsarr=None
        else:
            elstrlist, el_gun=elements_elstr(elstr)
            if len(el_gun)>3:#if there are more than 3 "real" elements use the 1st 3, if there are less than 3, elstrlist will already be filled to 3 with 'X'
                elstrlist=[elgun[i][0] for i in range(3)]
            elstrlist, compsarr=getcomps(h5path, h5groupstr, elstrlist=elstrlist, infotype=infotype)
        if compsarr is None:
            elstrlist, compsarr=getcomps(h5path, h5groupstr, infotype=infotype, num_els=3)
        return elstrlist, compsarr


def synthpeakshape(q, pk):
    return pk[1]*numpy.exp(-2.0*(q-pk[0])**2/pk[2]**2)


#assumed format is 1 text line and then a line for each peak tab-delimeted
#pointind phaseregion phaseconcs A B C neighs Q H W
def readsyntheticpeaks(path):
    f = open(path, "r")
    lines=f.readlines()
    f.close()
    pointind=[]
    comp=[]
    peaks=[]
    peaks_ind=[]
    for l in lines[1:]:
        p, garbage, a=l.partition('\t')
        garbage, garbage, a=a.partition('\t')
        garbage, garbage, a=a.partition('\t')
        a, garbage, b=a.partition('\t')
        b, garbage, c=b.partition('\t')
        c, garbage, q=c.partition('\t')
        garbage, garbage, q=q.partition('\t')
        q, garbage, h=q.partition('\t')
        h, garbage, w=h.partition('\t')
        w.strip()
        #print p, a, b, c, q, h, w
        p=eval(p)
        if p in pointind:
            peaks_ind+=[[eval(q), eval(h), eval(w)]]
        else:
            pointind+=[p]
            comp+=[[eval(a), eval(b), eval(c)]]
            peaks+=[peaks_ind]
            peaks_ind=[[eval(q), eval(h), eval(w)]]
    peaks+=[peaks_ind]
    peaks=peaks[1:]
    return pointind, comp, peaks

def createsynthetich5_peaktxt(h5path, peaktxtpath, elstr='ABC'):

    pointind, comp, pklist=readsyntheticpeaks(peaktxtpath)

    comp=numpy.float32(comp)
    if pointind!=range(len(pointind)):
        print 'ABORTED: the list of point indeces is required to be 0, 1, 2, ...'
        return 'ABORTED: the list of point indeces is required to be 0, 1, 2, ...'
    grid=[-30., 60./len(pointind), len(pointind)]
    cmd='a2scan'
    wl=.02
    cal=[0, 0, 500., 0, 0, 0]
    al=46.
    c=0.
    b='min'
    attrdict={'pointlist':pointind, 'command':cmd, 'xgrid':grid, 'zgrid':grid, 'wavelength':wl, 'cal':cal, 'alpha':al, 'counter':c, 'elements':elstr, 'bcknd':b, 'chessrunstr':'', 'imapstr':'/2008NovDec/imap/16,0.05,1.560e3', 'chimapstr':'', 'killmapstr':'', 'qimagestr':'', 'chiimagestr':'', 'dqchiimagestr':''}

    h5file=h5py.File(h5path, mode='w')
    h5groupstr='1'
    h5file.attrs['defaultscan']=h5groupstr
    h5grp=h5file.create_group(h5groupstr)
    h5grp=h5grp.create_group('analysis')
    h5mar=h5grp.create_group('mar345')
    h5depprof=h5grp.create_group('depprof')
    h5file.close()

    writeattr(h5path, h5groupstr, attrdict)

    h5file=h5py.File(h5path, mode='r+')
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
    h5mar=h5file['/'.join((h5groupstr, 'analysis', getxrdname(h5analysis)))]
    h5depprof=h5file['/'.join((h5groupstr, 'analysis/depprof'))]

    if 'icounts' in h5mar:
        qgrid=h5mar['icounts'].attrs['qgrid']
    else:
        qgrid=getimapqgrid(h5analysis.attrs['imapstr'], imap=False)
    qvals=numpy.float32(q_qgrid_ind(qgrid))

    icounts=[]
    maxnumpks=0
    for pks in pklist:
        maxnumpks=max(maxnumpks, len(pks))
        pattern=numpy.zeros(qvals.shape, dtype='float32')
        for pk in pks:
            pattern+=synthpeakshape(qvals, pk)
        icounts+=[pattern]
    icounts=numpy.float32(icounts)

    pkssavearr=[]
    for pks in pklist:
        pks=[[pk[0], pk[2], pk[1]] for pk in pks]#synthpeaks file has posn,height, width but pkcounts is posn,width,height
        pks+=[[numpy.nan, numpy.nan, numpy.nan] for i in range(maxnumpks-len(pks))]
        pkssavearr+=[pks]

    pkssavearr=numpy.float32(pkssavearr)
    h5mar.create_dataset('synthpks', data=pkssavearr)

    for count, arr in enumerate(comp.T):
        h5depprof.create_dataset('molfracgun%d' %count, data=arr)

    elstrslist, garbage=elements_elstr(elstr)

    h5depprof.attrs['symbol']=elstrslist

    h5depprof.attrs['guninds']=range(len(elstrslist))

    h5ic=h5mar.create_dataset('icounts', data=icounts)
    h5ic.attrs['qgrid']=qgrid
    h5ifc=h5mar.create_dataset('ifcounts', data=icounts)
    h5ifc.attrs['qgrid']=qgrid

    h5file.close()


def createh5_txtfiles(h5path, txtpath,  headerlines=0, elstr='ABC'):
    dirname, fname=os.path.split(txtpath)
    a, b, fext=fname.rpartition('.')
    ind=-1
    while a[ind].isdigit():
        ind-=1
    if ind==-1:
        print 'problem with file format. expecting name#.ext where # is an integer'
    rootname=a[:ind+1]
    files=os.listdir(dirname)
    file_num=[[f, eval(f.partition(rootname)[2].rpartition('.')[0])] for f in files if f.startswith(rootname) and f.endswith(fext)]
    files=map(operator.itemgetter(0),sorted(file_num, key=operator.itemgetter(1)))
    xvals=[]
    yvals=[]
    for path in files:
        print 'reading: ', path
        x, y, type=readplotso(os.path.join(dirname, path).replace('\\','/'), headerlines=headerlines)
        xvals+=[x]
        yvals+=[y]
    nvals=numpy.uint16([len(x) for x in xvals])
    nval=numpy.min(nvals)
    if not numpy.all(nvals==nval):
        print 'WARNING - not all datasets were the same legnth - datasets will be truncated to the shortest regardless of the alignment of the measurement axes'
    xvals=[x[:nval] for x in xvals]
    yvals=[y[:nval] for y in yvals]

    xvals=numpy.float32(xvals)
    yvals=numpy.float32(yvals)
    if len(xvals)>1 and not numpy.all(xvals[1:,:]==xvals[:-1,:]):
        print 'WARNING: not all xvals are the same - just using first one'
    qgrid=qgrid_minmaxnum(xvals[0, 0], xvals[0, -1], xvals.shape[1])
    print 'assessed qgrid:', qgrid
    pointind=range(xvals.shape[0])
    grid=[-30., 60./len(pointind), len(pointind)]
    cmd='a2scan'
    wl=.02
    cal=[0, 0, 500., 0, 0, 0]
    al=46.
    c=0.
    b='min'
    attrdict={'pointlist':pointind, 'command':cmd, 'xgrid':grid, 'zgrid':grid, 'wavelength':wl, 'cal':cal, 'alpha':al, 'counter':c, 'elements':elstr, 'bcknd':b, 'chessrunstr':'', 'imapstr':'', 'chimapstr':'', 'killmapstr':'', 'qimagestr':'', 'chiimagestr':'', 'dqchiimagestr':''}

    h5file=h5py.File(h5path, mode='w')
    h5groupstr='1'
    h5file.attrs['defaultscan']=h5groupstr
    h5grp=h5file.create_group(h5groupstr)
    h5grp=h5grp.create_group('analysis')
    h5mar=h5grp.create_group('mar345')
    #h5depprof=h5grp.create_group('depprof')
    h5file.close()

    writeattr(h5path, h5groupstr, attrdict)

    h5file=h5py.File(h5path, mode='r+')
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
    h5mar=h5file['/'.join((h5groupstr, 'analysis', getxrdname(h5analysis)))]
    #h5depprof=h5file['/'.join((h5groupstr, 'analysis/depprof'))]

    h5ic=h5mar.create_dataset('icounts', data=yvals)
    h5ic.attrs['qgrid']=qgrid
    h5file.close()


def exportpeaklist(h5path, h5groupstr, runpath):
    pointlist, peakinfo=getpeaksinrange(h5path, h5groupstr, indlist=None, returnonlyq=False, returnonlytallest=False)
    neighbors=getneighbors(h5path, h5groupstr)
    nbool=not neighbors is None
    if nbool:
        lines=['PointInd\tNeighborIndeces\tQpons\tGaussSigma\tHeight']
    else:
        lines=['PointInd\tQpons\tGaussSigma\tHeight']
    for ind, pk in zip(pointlist, peakinfo):
        lstr='%d' %ind
        if nbool:
            nstr=','.join(['%d' %n for n in neighbors[ind]])
            lstr='\t'.join((lstr, nstr))
        for n in pk[:3]:
            lstr='\t'.join((lstr, numtostring(n, 4)))
        lines+=[lstr]

    writestr='\n'.join(lines)

    savename='_'.join((os.path.split(h5path)[1][0:-3], h5groupstr, 'peaklist.txt'))
    filename=os.path.join(runpath,savename).replace('\\','/')
    fout = open(filename, "w")
    fout.write(writestr)
    fout.close()

def getneighbors(h5path, h5groupstr):
    h5file=h5py.File(h5path, mode='r')
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
    if not 'neighbors' in h5analysis:
        return None
    neigharr=readh5pyarray(h5analysis['neighbors'])
    neighlist=[]
    for n in neigharr:
        neighlist+=[list(n[n!=32767])]
    return neighlist

def saveneighbors(h5path, h5groupstr, neighbors, pardict={}):#len(neighbors ) should be the numpts in experiment
    maxnumneighs=max([len(n) for n in neighbors])
    savearr=numpy.ones((len(neighbors), maxnumneighs), dtype='uint16')*32767
    for count, n in enumerate(neighbors):
        savearr[count, :len(n)]=numpy.uint16(n)
    h5file=h5py.File(h5path, mode='r+')

    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
    if 'neighbors' in h5analysis:
        del h5analysis['neighbors']

    h5neighbors=h5analysis.create_dataset('neighbors', data=savearr)
    for k, v in pardict.iteritems():
        print k, v, type(k), type(v)
        h5neighbors.attrs[k]=v
    h5file.close()

def buildnewscan(h5path, h5groupstr, newscandict):
    xrdname=newscandict['xrdname']
    
    h5file=h5py.File(h5path, mode='r+')
    h5root=h5file.create_group(h5groupstr)
    h5analysis=h5root.create_group('analysis')
    measpath='/'.join((h5groupstr,'measurement'))
    measpath_copyfrom='/'.join((newscandict['sourcename'],'measurement'))
    anpath_copyfrom='/'.join((newscandict['sourcename'],'analysis'))
    h5file.copy(measpath_copyfrom, measpath)
    h5measurement=h5file[measpath]
    for k, v in h5file[anpath_copyfrom].attrs.iteritems():
        h5analysis.attrs[k]=v
    for ind, newname, newind in zip(newscandict['ind_tobereplaced'], newscandict['newimage_scanname'], newscandict['newimage_ind']):#"new" refers to the replacement
        h5measnew=h5file['/'.join((newname,'measurement'))]
        h5measurement[xrdname+'/counts'][ind, :, :]=h5measnew[xrdname+'/counts'][newind, :, :]
        if 'MCA/counts' in h5measurement and 'MCA/counts' in h5measnew:
            h5measurement['MCA/counts'][ind, :]=h5measnew['MCA/counts'][newind, :]
        if 'scalar_data/Seconds' in h5measnew:
            h5analysis.attrs['acquisition_time'][ind]=h5measnew['scalar_data/Seconds'][newind]
        for item in h5measurement['scalar_data'].iterobjects():
            itemname=item.name.rpartition('/')[2]
            if (not itemname in ['samx', 'samz']) and isinstance(item,h5py.Dataset) and len(item.shape)==1 and itemname in h5measnew['scalar_data']:#replace thinks like IC counts but not x,z position
                item[ind]=h5measnew['scalar_data/%s' %itemname][newind]


    for grpname, attr in zip(newscandict['appendscan_name'], newscandict['appendscan_attr']):
        h5analysis.attrs['command']='USER-COMPILED'
        #xgrid and zgrid are nto changed and are no longer valid
        numappendpts=len(attr['x'])
        h5measnew=h5file['/'.join((grpname,'measurement'))]
        h5analysis.attrs['acquisition_shape']=(numpy.prod(numpy.uint16(h5analysis.attrs['acquisition_shape']))+numappendpts,)
        h5analysis.attrs['x']=numpy.append(numpy.float32(h5analysis.attrs['x']), numpy.float32(attr['x']))
        h5analysis.attrs['z']=numpy.append(numpy.float32(h5analysis.attrs['z']), numpy.float32(attr['z']))
        if 'acquisition_time' in attr:
            h5analysis.attrs['acquisition_time']=numpy.append(numpy.float32(h5analysis.attrs['acquisition_time']), numpy.float32(attr['acquisition_time']))
        elif 'scalar_data/Seconds' in h5measnew:
            h5analysis.attrs['acquisition_time']=numpy.append(numpy.float32(h5analysis.attrs['acquisition_time']), numpy.float32(h5measnew['scalar_data/Seconds'][:]))
        else:
            h5analysis.attrs['acquisition_time']=numpy.append(numpy.float32(h5analysis.attrs['acquisition_time']), numpy.ones(numappendpts, dtype='float32'))

        h5mar=h5measurement[xrdname]
        arr1=readh5pyarray(h5mar['counts'])
        del h5mar['counts']# this way it is deleted no matter what and it will be rewritten if there is data to append. this ensure that all arrays end up the right length.
        if (xrdname+'/counts') in h5measnew:
            arr2=readh5pyarray(h5measnew[xrdname+'/counts'])
            arr1=numpy.append(arr1, arr2, axis=0)
            h5mar.create_dataset('counts', data=arr1)

        if 'MCA/counts' in h5measurement:
            h5mca=h5measurement['MCA']
            arr1=readh5pyarray(h5mca['counts'])
            del h5mca['counts']
            if 'MCA/counts' in h5measnew:
                arr2=readh5pyarray(h5measnew['MCA/counts'])
                arr1=numpy.append(arr1, arr2, axis=0)
                h5mca.create_dataset('counts', data=arr1)

        h5sd=h5measurement['scalar_data']
        for item in h5sd.values():
            itemname=item.name.rpartition('/')[2]
            if isinstance(item,h5py.Dataset) and len(item.shape)==1:
                del h5sd[itemname]
                if itemname in h5measnew['scalar_data']:
                    arr1=readh5pyarray(item)
                    arr2=readh5pyarray(h5measnew['scalar_data/%s' %itemname])
                    arr1=numpy.append(arr1, arr2, axis=0)
                    h5sd.create_dataset(itemname, data=arr1)
    h5file.close()

def initializescan(h5path, h5groupstr, bin=3):
    h5file=h5py.File(h5path, mode='r+')
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
    h5mar=h5file['/'.join((h5groupstr, 'analysis', getxrdname(h5analysis)))]
    h5marcounts=h5file['/'.join((h5groupstr,'measurement', getxrdname(h5analysis), 'counts'))]
    h5analysis.attrs['bin']=bin
    attrdict=getattr(h5path, h5groupstr)
    if not ('bminanomf' in h5mar):
        bminanomfinit=numpy.ones((numpts_attrdict(attrdict), 3),  dtype='float32')*(-1.0)
        h5mar.create_dataset('bminanomf', data=bminanomfinit)
    print 'binning data'
    pointlist=[]
    if 'countsbin%d' %bin in h5mar:
        del h5mar['countsbin%d' %bin]
    countsbin=h5mar.create_dataset('countsbin%d' %bin, (h5marcounts.shape[0],h5marcounts.shape[1]//bin,h5marcounts.shape[2]//bin), dtype=h5marcounts.dtype)
    z=numpy.zeros((h5marcounts.shape[1]//bin,h5marcounts.shape[2]//bin), dtype=h5marcounts.dtype)
    for count, image in enumerate(h5marcounts):
        data=image[:, :]
        if data.max()>0:
            pointlist+=[count]
            countsbin[count, :, :]=binimage(data, bin)
        else:
            countsbin[count, :, :]=z[:, :]
    h5analysis.attrs['pointlist']=pointlist
    h5file.attrs['defaultscan']=str(h5groupstr)
    if 'min' in attrdict['bcknd']:
        initbcknd='min'
    elif 'lin' in attrdict['bcknd']:
        initbcknd='min'
    else:
        initbcknd='ave'
    print 'calculating ',  initbcknd, 'background - last step of data initialization'
    calcbcknd(h5path=h5path, h5groupstr=h5groupstr, bcknd=initbcknd, bin=bin)
    h5file.close()

def readxrfinfodatabase():
    f=open(XRFINFOpath(), mode='r')
    lines=f.readlines()
    f.close()

    entries=[]
    currentdict={}
    currentval=None
    lines+=['  ']#toadd the last dict to entries
    for l in lines:
        l=l.strip()
        if len(l)==0:
            if not currentval is None:
                if len(currentval)==1:
                    currentval=currentval[0]
                currentdict[k]=currentval
                currentval=None
                entries+=[copy.deepcopy(currentdict)]
                currentdict={}
        elif l.startswith('['):
            if not currentval is None:
                if len(currentval)==1:
                    currentval=currentval[0]
                currentdict[k]=currentval
            currentval=[]
            k=l[1:].partition(']')[0]
        else:
            lineval=[]
            c=l
            while len(c)>0:
                a, b, c=c.partition('\t')
                a=a.strip()
                c=c.strip()
                try:
                    val=eval(a)
                except:
                    val=a
                lineval+=[val]
            if len(lineval)==1:
                lineval=lineval[0]
            currentval+=[lineval]
    return entries


#getpeaksinrange('E:/CHESS2008/2008CHESSh5analysis/20081121bsub3RuPtX.dat.h5', '2', [11,19,20,21,29,30,31,39,40,41,49,50,51,59,60,61,69], 32, 32.5, performprint=True)

def myexpformat(x, pos=0):
    for ndigs in range(6):
        lab=(('%.'+'%d' %ndigs+'e') %x).replace('e+0','e').replace('e+','e').replace('e0','')
        if eval(lab)==x:
            return lab
    return lab
#ExpTickLabels=FuncFormatter(myexpformat)
#ax.xaxis.set_major_formatter(ExpTickLabels)


pointlist=[11,20,21,28,29,30,31,38,39,40,41,48,49,50,51,58,59,60,61,69]
def runme():
    return testwavetrans1d('/mnt/SharedData/CHESS2008/2008CHESSh5analysis/20081121bsub3RuPtX.dat.h5','2','0.1,1.18,23_18,0.1,750_16,0.05,1.540e3')
def testwavetrans1d(h5path, h5groupstr, wavesetname):#wavetrans qgrid can be subset of icounts qgrid but not vice versa
#    print "h5path='", h5path, "'"
#    print "h5groupstr='", h5groupstr, "'"
#    print "wavesetname='", wavesetname, "'"
    h5wave=WAVESET1dFILE()

    wavegrp=h5wave[wavesetname]
    waveset=wavegrp['waveset'][:, :, :]
    waveqgrid=wavegrp.attrs['qgrid']
    print 'wave grid', waveqgrid
    h5file=h5py.File(h5path, mode='r')
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
    h5mar=h5file['/'.join((h5groupstr, 'analysis', getxrdname(h5analysis)))]

    wtgrp=h5mar['wavetrans1d']
    qscalegrid=wavegrp.attrs['qscalegrid']
    qposngrid=wavegrp.attrs['qposngrid']
    print 'wave grid', qscalegrid, qposngrid
    h5wave.close()

    pointlist=[11,20,21,28,29,30,31,38,39,40,41,48,49,50,51,58,59,60,61,69]


    a, b, c =waveset.shape # num scales, num posn, length of data
    #dfltarr=numpy.empty((a, b), dtype='float32')*numpy.nan

    icountspoint=h5mar['icounts']
    qgrid=icountspoint.attrs['qgrid']
    print 'qgrid', qgrid
    icind=numpy.array([qval in q_qgrid_ind(waveqgrid) for qval in q_qgrid_ind(qgrid)])
    icounts=icountspoint[:, :]
    ridgespoint=readh5pyarray(wtgrp['ridges'])

    wt=numpy.zeros((icountspoint.shape[0], a, b), dtype='float32')
    h5file.close()
    TIMESTART=time.time()
    #for ind in set(range(wt.shape[0]))-set(pointlist):
#    for ind in range(wt.shape[0]):
#        wt[ind, :, :]=dfltarr[:, :]


    for pointind in pointlist:
        data=icounts[pointind][icind]
        #wt[pointind, :, :]=numpy.float32([[(vec*data).sum() for vec in arr] for arr in waveset])
        wt[pointind, :, :]=numpy.float32([[(vec*data).sum()/scale for vec in arr] for arr, scale in zip(waveset, scale_scalegrid_ind(qscalegrid))])


    minridgelength=1
    noiselevel=20.
    maxqscale_localmax=1.5
    minridgewtsum=100.
    verbose=False


#    h5file=h5py.File(h5path, mode='r+')
#    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
#    h5mar=h5file['/'.join((h5groupstr, 'analysis', getxrdname(h5analysis)))]
#    wtgrp=h5mar['wavetrans1d']
    #qscalegrid=wtgrp.attrs['qscalegrid']
    qscalevals=scale_scalegrid_ind(qscalegrid)
    #qposngrid=wtgrp.attrs['qposngrid']
    qposnint=qposngrid[1]

    qsindlist=[2*max(int(numpy.ceil(1.*qs/qposnint)), 1) for qs in qscalevals[::-1]]
    #pointlist=h5analysis.attrs['pointlist']


    ridgeqscalevals=scale_scalegrid_ind(qscalegrid)[::-1] #ordered big->small

    ridgescalecritind=numpy.where(ridgeqscalevals<=maxqscale_localmax)[0]

    ridgescalecritind=ridgescalecritind[0] #takes the last because these are in decreasing order now

    ridges_pointlist=[]
    peaks_pointlist=[]
    for pointind in pointlist:
        temp=wt[pointind, :, :]#reverse first index so that it goes from widest to smallest scale
        wtrev=temp[::-1, :]
        perform_ridges_wavetrans1d(wtrev, qsindlist, noiselevel, numscalesskippedinaridge=1.5)

        ridges=ridgespoint[pointind, :, :]
        peaks_pointlist+=[perform_peaks_ridges1d(temp, ridges, ridgescalecritind=ridgescalecritind, minridgelength=minridgelength, minridgewtsum=minridgewtsum, verbose=verbose)]

    TIMESTOP=time.time()

    print 'time elapsed=', TIMESTOP-TIMESTART
    print 'num peaks=', numpy.sum(numpy.array([len(b) for b in peaks_pointlist]))
    return peaks_pointlist

def readpdffile(pdfentriespath):
    fin = open(pdfentriespath, "r")
    lines=fin.readlines()
    fin.close()
    pdfname=[]
    pdflist=[]
    for ln in lines:
        name, garbage, liststr=ln.partition(':')
        try:
            temp=eval(liststr.strip())
            if len(temp)==2:
                temp=numpy.float32(temp).T
            else:
                temp=numpy.float32(temp)
            temp[:, 1]/=numpy.max(temp[:, 1])

            pdfname+=[name]
            pdflist+=[temp]
        except:
            print 'format error in pdf entry ', liststr
    return pdfname, pdflist
    
def xrdraw_dezing_rescale(h5path, h5groupstr=None, h5grppath=None, dezingbool=False, normdsetname=None, multval=None, outlier_nieghbratio=None):
    h5file=h5py.File(h5path, mode='r+')
    if not h5groupstr is None:
        h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
        h5marcounts=h5file['/'.join((h5groupstr,'measurement/'+getxrdname(h5analysis)+'/counts'))]
        h5sd=h5file['/'.join((h5groupstr,'measurement', 'scalar_data'))]
    else:
        h5analysis=None
        h5marcounts=h5file[h5grppath]['counts']
        if not normdsetname is None:
            h5sd=(h5file[h5grppath].parent)['scalar_data']
    marcounts=readh5pyarray(h5marcounts)
    if multval is None:
        multval=1
    multval=numpy.array([multval], dtype=marcounts.dtype)[0]
    for count, arr in enumerate(marcounts):
        if not normdsetname is None:
            m=multval/h5sd[normdsetname][count]
        else:
            m=multval
        if dezingbool:
            arr=dezing(arr, critval=arr.max())
        if not outlier_nieghbratio is None:
            arr=removesinglepixoutliers(arr, critratiotoneighbors=outlier_nieghbratio)
        marcounts[count, :, :]=(arr*m)[:, :]
    h5marcounts[:, :, :]=marcounts[:, :, :]
    for k, v in zip(['mod_dezing', 'mod_normbyscalar', 'mod_multiplier', 'mod_outlier_neighbratio'], [dezingbool, normdsetname, multval, outlier_nieghbratio]):
        print k, v
        if v is None:
            continue
        h5marcounts.attrs[k]=v
    if not h5analysis is None:
        updatelog(h5analysis,  ''.join(('raw XRD data modified using dezingbool=%s, normdsetname=%s, multval=%s' %(`dezingbool`, `normdsetname`,  `multval`), '. finished ', time.ctime())))
    h5file.close()

def CopyLinBckndData(h5path, h5groupstr, h5path_from, h5groupstr_from):
    h5file=h5py.File(h5path, mode='r+')
    h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
    h5mar=h5file['/'.join((h5groupstr, 'analysis', getxrdname(h5analysis)))]
    
    h5file_from=h5py.File(h5path_from, mode='r')
    h5analysis_from=h5file_from['/'.join((h5groupstr_from, 'analysis'))]
    h5mar_from=h5file_from['/'.join((h5groupstr_from, 'analysis', getxrdname(h5analysis_from)))]
    
    dellist=[]
    for pnt in h5mar.itervalues():
        if isinstance(pnt,h5py.Dataset):
            temp=pnt.name.rpartition('/')[2]
            if temp.startswith('blin'):
                dellist+=[temp]
    for temp in dellist:
        del h5mar[temp]

    anycopied=False
    for pnt in h5mar_from.itervalues():
        if isinstance(pnt,h5py.Dataset) and (pnt.name.rpartition('/')[2]).startswith('blin'):
            h5file.copy(pnt, h5mar[pnt.name.rpartition('/')[2]])
            anycopied=True
    
    if anycopied:
        updatelog(h5analysis,  ''.join(('LinBcknd arrays and attrs copied from %s %s' %(h5path_from, h5groupstr_from), '. finished ', time.ctime())))
        h5file.close()
        h5file_from.close()
    else:
        h5file.close()
        h5file_from.close()
        print 'CopyFailed: No LinBkcnd arrays were found'
        return 'CopyFailed: No LinBkcnd arrays were found'
