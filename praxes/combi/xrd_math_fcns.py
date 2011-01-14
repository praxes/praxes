import copy

import matplotlib.delaunay as dlny
import numpy
import scipy
import scipy.optimize
import scipy.interpolate

from .xrd_diffraction_conversion_fcns import *


def numtostring(x, n=0): #exponential notation with n significnat digits. if n not specified then trivial string conversion
    if n < 1:
        return str(x)
    return "%.*e" % (n-1, x)

def polarr_cart(x, y):
    x=1.0*x
    y=1.0*y
    return numpy.sqrt(x**2+y**2)

def polart_cart(x, y):
    x=1.0*x
    y=1.0*y
    if x==0:
        return (y!=0)*(numpy.pi/2+numpy.pi*(y<0))
    if x<0:
        return numpy.pi-numpy.arctan(-1.0*y/x)
    if y<0:
        return 2.0*numpy.pi-numpy.arctan(-1.0*y/x)
    return numpy.arctan(y/x)

def polar_cart(x,y):#this is the function to call and excepts floats or arrays
    if isinstance(x, numpy.ndarray):
        return polarr_cart(x, y), numpy.float32(map(polart_cart, x, y))
    return polarr_cart(x, y), polart_cart(x, y)

def firstder(y, dx=1.0):#takes an array of values y and the dx corresponding to 1 index and returns same length array of the 5-point stencil of second derivative, copying the 2 values on each end
    secd=(8.0*(y[3:-1]-y[1:-3])+y[:-4]-y[4:])/(12.0*dx)
    temp=numpy.empty(y.shape, dtype=numpy.float32)
    temp[:2]=secd[0]
    temp[-2:]=secd[-1]
    temp[2:-2]=secd[:]
    return temp

def secder(y, dx=1.0):#takes an array of values y and the dx corresponding to 1 index and returns same length array of the 5-point stencil of second derivative, copying the 2 values on each end
    secd=((-30.0)*y[2:-2]+16.0*(y[1:-3]+y[3:-1])-(y[:-4]+y[4:]))/(12.0*dx**2)
    temp=numpy.empty(y.shape, dtype=numpy.float32)
    temp[:2]=secd[0]
    temp[-2:]=secd[-1]
    temp[2:-2]=secd[:]
    return temp

def arrayder_x(arr, dx=1.0):
    return numpy.array([firstder(col, dx) for col in arr.T]).T

def arrayder_y(arr, dx=1.0):
    return numpy.array([firstder(col, dx) for col in arr])

def arrayder_xx(arr, dx=1.0):  #9-point stencil error order dx**2. outer ring of values are copied from inner
    siz=arr.size
    #                  +1, +1                        -1,+1                     +1,0                          -1,0                  +1, -1                      -1, -1                       0, 1                        0,0                   0, -1
    secd=(arr[2:siz, 2:siz]+arr[0:-2, 2:siz]+arr[2:siz, 1:-1]+arr[0:-2, 1:-1]+arr[2:siz, 0:-2]+arr[0:-2, 0:-2]-2.0*(arr[1:-1, 2:siz]+arr[1:-1, 1:-1]+arr[1:-1, 0:-2]))/(3.0*dx**2)
    temp=numpy.empty(arr.shape, dtype=numpy.float32)
    temp[1:-1, 1:-1]=secd[:, :]
    temp[1:-1,0]=secd[:, 0]
    temp[1:-1,-1]=secd[:, -1]
    temp[0, :]=temp[1, :]
    temp[-1, :]=temp[-2, :]
    return temp

def arrayder_yy(arr, dx=1.0):  #9-point stencil error order dx**2. outer ring of values are copied from inner
    return arrayder_xx(arr.T, dx).T

def arrayder_xy(arr, dx=1.0):  #7-point stencil error order dx**2. outer ring of values are copied from inner
    siz=arr.size
    #                  +1, +1                          +1,0                          -1,0                -1, -1                       0, 1                        0,0                   0, -1
    secd=(-arr[2:siz, 2:siz]+arr[2:siz, 1:-1]+arr[0:-2, 1:-1]-arr[0:-2, 0:-2]+arr[1:-1, 2:siz]-2.0*arr[1:-1, 1:-1]+arr[1:-1, 0:-2])/(-2.0*dx**2)
    temp=numpy.empty(arr.shape, dtype=numpy.float32)
    temp[1:-1, 1:-1]=secd[:, :]
    temp[1:-1,0]=secd[:, 0]
    temp[1:-1,-1]=secd[:, -1]
    temp[0, :]=temp[1, :]
    temp[-1, :]=temp[-2, :]
    return temp

#def arrayder_xy(arr, dx):  #4-point stencil error order dx**2. outer ring of values are copied from inner
#    siz=arr.size
#    #                  +1, +1                    -1, -1                            1,-1                   -1, 1
#    secd=(-arr[2:siz, 2:siz]-arr[0:-2, 0:-2]-2.0*arr[2:siz, 0:-2]+arr[0:-2, 2:siz])/(4.0*dx**2)
#    temp=numpy.empty(arr.shape, dtype=numpy.float32)
#    temp[1:-1, 1:-1]=secd[:, :]
#    temp[1:-1,0]=secd[:, 0]
#    temp[1:-1,-1]=secd[:, -1]
#    temp[0, :]=temp[1, :]
#    temp[-1, :]=temp[-2, :]
#    return temp

def chimap_gen(qimage, chiimage, chigrid): #chigrid in degrees, returns chimap in degrees
    chiimageabsdeg=numpy.abs(chiimage*180.0/numpy.pi)
    chiends=slotends_qgrid(chigrid)
    chimap=numpy.zeros(shape=chiimage.shape, dtype='int16')
    for count, (chimin, chimax) in enumerate(zip(chiends[:-1], chiends[1:])):
        chimap[(chiimageabsdeg>=chimin)&(chiimageabsdeg<chimax)]=count+1
    chimap[chiimage<0]*=-1
    return chimap

def imap_gen(qimage, qgrid):
    qends=slotends_qgrid(qgrid)
    imap=numpy.zeros(shape=qimage.shape, dtype='uint16')
    for count, (qmin, qmax) in enumerate(zip(qends[:-1], qends[1:])):
        imap[(qimage>=qmin)&(qimage<=qmax)]=count+1
    return imap

def interp(func, y, xcrit):
    #func must be monotonic, y should be at least length 3
    trylist=list(y)
    trylist.sort
    tryans=[func(i) for i in trylist]
    i=0
    while i<len(trylist)-1:
        if tryans[i]==tryans[i+1]:
            del trylist[i]
            del tryans[i]
        else:
            i+=1
    maxtries=20
    tries=0
    while tries<maxtries and not(len(trylist)>=4 and xcrit>=min(tryans) and xcrit<=max(tryans)):
        tries+=1
        hightry=trylist[-1]*(1.0+0.2*tries**2)
        lowtry=trylist[0]/(1.0+0.2*tries**2)
        highans=func(hightry)
        lowans=func(lowtry)
        if lowans!=tryans[0]:
            trylist=[lowtry]+trylist
            tryans=[lowans]+tryans
        if highans!=tryans[-1]:
            trylist=trylist+[hightry]
            tryans=tryans+[highans]

    if tries==maxtries:
        print 'interp problem'
        return None
    if tryans!=tryans.sort:
        trylist.sort
    print 'in interp', xcrit, tryans, trylist
    ycrit=scipy.interpolate.UnivariateSpline(tryans, trylist)(xcrit)[0]
    if numpy.isnan(ycrit):
        print 'interp problem'
        return None
    else:
        return ycrit

def qq_gen(innn): #innn should be array of intensity values dtype='float32'
    slots=innn.size
    zer=numpy.ndarray.tolist(numpy.zeros(slots,  dtype='float32'))
    return numpy.array([zer[:i]+numpy.ndarray.tolist(innn[i]*innn[i:]) for i in xrange(slots)], dtype='float32').T

def intbyarray(data, imap, dqchiimage, slots=None):   #data must be a square array, optionally dtype='uint16', map is same size as data with each pixel value v, v=0->ignored, else included in integration bin v-1
    if slots is None:
        slots=imap.max()
    data=numpy.float32(numpy.abs(dqchiimage)*data)
    ans=numpy.array([(data[imap==i]).sum() for i in xrange(1, slots+1, 1)])
    ans[numpy.where(numpy.isnan(ans))]=0.0
    return ans

def integrationnormalization(killmap, imap, dqchiimage, slots=None):#this pretty much is the reciprocal of the integration of killmap so that haveing a small number of pixels in certain q-range doesn't affect magnitude of icounts
    if slots is None:
        slots=imap.max()
    data=numpy.float32(numpy.abs(dqchiimage)*killmap)
    ans=numpy.array([(data[imap==i]).sum() for i in xrange(1, slots+1, 1)])
    ans[numpy.where(numpy.isnan(ans))]=0.0
    ans[ans<0]=0.0#shouldn't be necessary
    ans[ans>0]=1/ans[ans>0]
    return ans

def binimage(data, bin=3, zerokill=False, mapbin=None): #data is square array, dtype='uint16', int16 or float32. averages bin by bin sections of the array and returns smaller array    #mapbin changes the grid
    size=data.shape[0]
    if zerokill:
        nonzeromap=binboolimage(data!=0, bin=bin)
    if 'float' in str(data.dtype): #this isn't compatiible with mapbin:
        b = numpy.float32([data[:, i:i+bin].sum(axis=1) for i in xrange(0, size, bin)])
        ans=numpy.float32(numpy.array([b[:, k:k+bin].sum(axis=1) for k in xrange(0, size, bin)])/bin**2)
        if zerokill:
            ans*=nonzeromap
    else:
        b = numpy.array([data[:, i:i+bin].sum(axis=1, dtype='int32') for i in xrange(0, size, bin)])
        if data.dtype=='bool':
            ans=numpy.bool_(numpy.array([b[:, k:k+bin].sum(axis=1, dtype='int32') for k in xrange(0, size, bin)])//bin**2)
        else:
            ans=numpy.array(numpy.array([b[:, k:k+bin].sum(axis=1, dtype='int32') for k in xrange(0, size, bin)])//bin**2, dtype=data.dtype)
        if zerokill:
            ans*=nonzeromap
        if not (mapbin is None):
            ans=numpy.array((numpy.int32(ans)-1)//mapbin+1, dtype=data.dtype)
    return ans

def mapbin(data, mapbin=3):
    return (data-1)//mapbin+1

def unbinimage(data, bin=3):
    size=data.shape[0]*bin
    d=numpy.empty((size, size), dtype='uint16')
    a=numpy.zeros(bin, dtype='uint16')
    return numpy.array([(numpy.array([a+i for i in data[j//bin]])).flatten() for j in range(bin*data.shape[0])])

def binboolimage(data, bin=3): #data is square array, dtype='bool'. every pixel in bin must be True for binned pixel to be True
    size=data.shape[0]
    b = numpy.array([data[:, i:i+bin].prod(axis=1, dtype='bool') for i in xrange(0, size, bin)], dtype='bool')
    return numpy.array([b[:, k:k+bin].prod(axis=1, dtype='bool') for k in xrange(0, size, bin)], dtype='bool')

def unbinboolimage(data, bin=3):
    size=data.shape[0]*bin
    d=numpy.empty((size, size), dtype='bool')
    a=numpy.zeros(bin, dtype='bool')
    return numpy.array([(numpy.array([a+i for i in data[j//bin]])).flatten() for j in range(bin*data.shape[0])])


def bckndsubtract(data, bckndarr, killmap=None, btype='minanom', banom_f_f=None,  banomcalc=None):
#data,bckndarr,killmap must be same size. banom will be adjusted to that size
#if btype is 'min' or 'ave' just calculates and returns - killmap can be None for this but must be passed otherwise
#if btype is 'minanom' and calculation of anomalous backnd and factors is to be avoided: pass banom_f_f=(banom,fmin,fanom)
#if btype is 'minanom' and calculation must happen do not pass banom_f_f ,  pass banomcalc=(imap,qgrid,attrdict, None or bimap, None or bqgrid, None or fraczeroed, None or factorprecision)  -don'e have to include trailing None's - also, in this case all the arrays must be full sized
#returns tuple (bcknd subtracted data) if no banom, fmin, fanom, calc done, otherwise (    , banom, fmin, fanom, bimap, bqgrid,fraczeroed)
# if 'minanom' then bckndarr is bmin
    if btype=='min' or btype=='ave':
        a=bckndarr>data
        data-=bckndarr
        data[a]=0
        if killmap is None:
            return (data, bckndarr)
        else:
            return (data*killmap, bckndarr*killmap)
    elif btype=='minanom':
        if banom_f_f is None or len(banom_f_f)!=3:
            bac=banomcalc
            while len(bac)<7:
                bac+=(None,)
            if (bac[3] is not None) and (bac[4] is not None):
                bimapqgridstr=', bimap=bac[3], bqgrid=bac[4]'
            else:
                bimapqgridstr=''
            if bimapqgridstr=='' and (bac[4] is not None):
                bimapqgridstr2=', bqgrid=bac[4]'
            else:
                bimapqgridstr2=''
            if bac[5] is not None:
                fzstr=', fraczeroed=bac[5]'
            else:
                fzstr=''
            if bac[6] is not None:
                fpstr=', factorprecision=bac[6]'
            else:
                fpstr=''
            cbbf=eval(''.join(('calc_bmin_banom_factors(data, bckndarr, killmap, bac[0], bac[1],bac[2]', bimapqgridstr, bimapqgridstr2, fzstr, fpstr, ')')))
            fmin=cbbf.fmin
            fanom=cbbf.fanom
            banom=cbbf.banom
            banomreturn=banom
            bimap=cbbf.bimap
            bqgrid=cbbf.bqgrid
            returnall=True
        else:
            returnall=False
            banom=banom_f_f[0]
            fmin=banom_f_f[1]
            fanom=banom_f_f[2]
        if data.shape[0]>banom.shape[0]:
            if (data.shape[0]%banom.shape[0])==0:
                banom=unbinimage(banom, data.shape[0]/banom.shape[0])
            else:
                print 'INCOMMENSURATE DATA ARRAY AND ANAMALOUS BACKGROUND ARRAY'
                return (data, )
        if data.shape[0]<banom.shape[0]:
            if (banom.shape[0]%data.shape[0])==0:
                banom=binimage(banom, banom.shape[0]/data.shape[0])
            else:
                print 'INCOMMENSURATE DATA ARRAY AND ANAMALOUS BACKGROUND ARRAY'
                return (data, )
        totbcknd=(fmin*bckndarr+fanom*banom)*killmap
        data*=killmap
        a=data<totbcknd
        data-=totbcknd
        data[a]=0
        if returnall:
            fracz=a.sum()/(killmap.sum())
            return (data, banom, fmin, fanom, bimap, bqgrid, fracz)
        else:
            return (data,totbcknd)
    else:
        print 'UNKNOWN BACKND TYPE IN BACKNDSUBTRACT'
        return (data, bckndarr)

class calc_bmin_banom_factors():
    def __init__(self, data, bmin, killmap, imap, qgrid, attrdict,  fraczeroed=0.005, factorprecision=0.005, bimap=None, bqgrid=None, qimage=None):
        #must pass either bimap or qimage.
        bin=3
        #everyhitng should be binned to same size specified as bin
        # if providing bimap must provide correct bqgrid - if bimap provided, will use that bin
        #data,bmin,killmap,imap must be full sized
        #factor precision is % not additive
        #takes an image with bmin subtracted and takes a bqgrid annulus and finds what constant value could be subtracted from that and satisfy frac zero. an image is interpolated from these values
        #this image is azimuthally symmetric and should be roughly the background from xrays that are fluoresced or diffracted by amorphous stuff like air. then there is trading between this type
        #of backnd and bmin to see how you weigh them to subtract the highest possible number of pixels from the image while keeping fraczeroed. other constraint is fbmin>=1
        if data.shape!=bmin.shape or data.shape!=killmap.shape or data.shape!=imap.shape :
            print 'calc_bmin_banom_factors NOT CURRENTLY SUPPORTING DIFFERENT ARRAY SHAPES'
        self.fz=fraczeroed
        self.fp=factorprecision
        self.center=numpy.float32(bincenterind_centerind(centerindeces_fit2dcenter(attrdict['cal']), bin))
        self.L=attrdict['cal'][2]
        self.wl=attrdict['wavelength']
        if bqgrid is None:
            minbinwidth=8  #this should be much larger than the widest features (peaks) not to be substracted
            b2=numpy.uint16(numpy.ceil((qgrid[2]-1)*1.0*qgrid[1]/minbinwidth))
#            b1=qgrid[1]*(qgrid[2]-1.0)/(b2-1) #put center of first and last bin same as qgrid but overall range wider
#            self.bqgrid=[qgrid[0], b1, b2]
            self.bqgrid=qgrid_minmaxnum(qgrid[0], minmaxint_qgrid(qgrid)[1], b2)
        else:
            self.bqgrid=bqgrid
        if (bimap is None) or (3450%bimap.shape[0]!=0):
            if qimage is None:
                print 'aborted because need to calculate bimap but cannot without qimage'
            self.bimap=imap_gen(qimage, self.bqgrid)
#            qslots=slotends_qgrid(self.bqgrid)
#            pixslots=pix_q(qslots, self.L,self.wl, psize=0.1*bin)
#            self.bimap=makeintmap(pixslots,self.center, size=(3450//bin))
        else:
            self.bimap=bimap

        self.bin=3450//self.bimap.shape[0]
        self.center=numpy.float32(bincenterind_centerind(centerindeces_fit2dcenter(attrdict['cal']), self.bin))
        self.killmap=killmap*(imap!=0)

        #print self.killmap.sum()

        self.data=data*self.killmap
        self.bmin=bmin*self.killmap
        self.killmap[self.data<self.bmin]=0 # do not count pixels that were already zeroed from bmin "zeroed" pixels are only those due to the bmin, banom wieghting
        self.data*=self.killmap
        self.bmin*=self.killmap
        self.bimap*=self.killmap
        self.numpix=self.killmap.sum()
        #print 'self.numpix', self.numpix

        self.bdata=self.data-self.bmin
        qvals=q_qgrid_ind(self.bqgrid)
        pixvalssq=pix_q(qvals, self.L,self.wl, psize=0.1*self.bin)**2

        bqmin=numpy.array([self.bqmin_gen(i+1) for i in range(self.bqgrid[2])])
        #print '**', bqmin
        self.banom_int=scipy.interpolate.UnivariateSpline(pixvalssq, bqmin)
        self.banom=self.banom_gen()
        nanlist=numpy.isnan(self.banom)
        if nanlist.sum()>0:
            print "INTERPOLATION ERROR making banom"
            self.banom[nanlist]=0
        banomcounts=self.banom.sum()
        if banomcounts==0:
            self.fmin=1.0
            self.fanom=0.0
        else:
            bmincounts=self.bmin.sum()
            delcounts=bmincounts*self.fp
            delfmin=delcounts/(1.0*bmincounts)
            delfanom=delcounts/(1.0*banomcounts)
            self.fmin=1.0
            self.fanom=1.0

            self.fanom=interp(self.fracz_fanom, numpy.array([0.8, 0.9, 1.0, 1.1, 1.2])*self.fanom, self.fz)


            if self.fanom is None:
                self.fanom=0
            else:
                if self.fanom<0:
                    self.fanom=0
                while (self.btot_gen(self.fmin+delfmin, self.fanom-delfanom)>self.data).sum() < (self.btot_gen(self.fmin, self.fanom)>self.data).sum():
                    self.fmin+=delfmin
                    self.fanom-=delfanom
                    trylist=numpy.array(range(4))*self.fp+1
                    temp=interp(self.fracz_fanom, trylist*self.fanom, self.fz)
                    if temp is None:
                        print "INTERPOLATION ERROR increasing fanom:", trylist
                        self.fanom=0
                        break
                    else:
                        self.fanom=temp
    #self.bimap, self.bqgrid, self.fmin, self.fanom,self.banom ready to be read
        totbcknd=self.btot_gen(self.fmin, self.fanom)
        #self.data*=self.killmap
        self.fracz=(totbcknd>self.data).sum()/numpy.float32(self.numpix)


    def fracz_fanom(self, fanom):
        return ((self.btot_gen(self.fmin, fanom)>self.data).sum())/numpy.float32(self.numpix)

    def bqmin_gen(self, slotnum):
        a=self.bdata[self.bimap==slotnum]
        a.sort()
        if a.size==0:
            return 0
        else:
            return a[numpy.uint16(a.size*self.fz)]

    def banom_gen(self):
        temp=numpy.array([[self.banom_int((i-self.center[1])**2+(j-self.center[0])**2)[0]  for i in range(3450/self.bin)]  for j in range(3450/self.bin)], dtype='int32')
        temp[temp<0]=0
        return numpy.uint16(temp)

    def btot_gen(self, fmin, fanom):
        return (self.bmin*fmin+self.banom*fanom)*self.killmap


#class calc_bmin_banom_factors():
#    def __init__(self, data, bmin, killmap, imap, qgrid, attrdict,  fraczeroed=0.005, factorprecision=0.005, bimap=None, bqgrid=None,  bin=3):
#        #3450/bin must be int
#        # if providing bimap must provide correct bqgrid - if bimap provided, will use that bin
#        #data,bmin,killmap,imap must be full sized
#        #factor precision is % not additive
#        #takes an image with bmin subtracted and takes a bqgrid annulus and finds what constant value could be subtracted from that and satisfy frac zero. an image is interpolated from these values
#        #this image is azimuthally symmetric and should be roughly the background from xrays that are fluoresced or diffracted by amorphous stuff like air. then there is trading between this type
#        #of backnd and bmin to see how you weigh them to subtract the highest possible number of pixels from the image while keeping fraczeroed. other constraint is fbmin>=1
#        self.fz=fraczeroed
#        self.fp=factorprecision
#        self.center=numpy.float32([attrdict['cal'][1], attrdict['cal'][0]])/bin#inverse order
#        self.L=attrdict['cal'][2]
#        self.wl=attrdict['wavelength']
#        if bqgrid is None:
#            minbinwidth=8  #this should be much larger than the widest features (peaks) not to be substracted
#            b2=numpy.uint16(numpy.ceil((qgrid[2]-1)*1.0*qgrid[1]/minbinwidth))
##            b1=qgrid[1]*(qgrid[2]-1.0)/(b2-1) #put center of first and last bin same as qgrid but overall range wider
##            self.bqgrid=[qgrid[0], b1, b2]
#            self.bqgrid=qgrid_minmaxnum(qgrid[0], minmaxint_qgrid(qgrid)[1], b2)
#        else:
#            self.bqgrid=bqgrid
#        if (bimap is None) or (3450%bimap.shape[0]!=0):
#            qslots=slotends_qgrid(self.bqgrid)
#            pixslots=pix_q(qslots, self.L,self.wl, psize=0.1*bin)
#            self.bimap=makeintmap(pixslots,self.center, size=(3450//bin))
#        else:
#            self.bimap=bimap
#
#        self.bin=3450//self.bimap.shape[0]
#        self.center=numpy.float32([attrdict['cal'][1], attrdict['cal'][0]])/self.bin#inverse order
#        self.killmap=binboolimage(killmap*(imap!=0), self.bin)
#
#        self.bimap*=self.killmap
#
#        self.data=binimage(data, self.bin)*self.killmap
#        self.bmin=binimage(bmin, self.bin)*self.killmap
#
#        self.numpix=self.killmap.sum()
#        self.fz+=(self.bmin>self.data).sum()/numpy.float32(self.numpix)
#        self.bdata=self.data-self.bmin
#        self.bdata[self.bmin>self.data]=0
#        qvals=q_qgrid_ind(self.bqgrid)
#        pixvalssq=pix_q(qvals, self.L,self.wl, psize=0.1*self.bin)**2
#
#        bqmin=numpy.array([self.bqmin_gen(i+1) for i in range(self.bqgrid[2])])
#        self.banom_int=scipy.interpolate.UnivariateSpline(pixvalssq, bqmin)
#        self.banom=self.banom_gen()
#        nanlist=numpy.isnan(self.banom)
#        if nanlist.sum()>0:
#            print "INTERPOLATION ERROR making banom"
#            self.banom[nanlist]=0
#        banomcounts=self.banom.sum()
#        if banomcounts==0:
#            self.fmin=1.0
#            self.fanom=0.0
#        else:
#            bmincounts=self.bmin.sum()
#            delcounts=bmincounts*self.fp
#            delfmin=delcounts/(1.0*bmincounts)
#            delfanom=delcounts/(1.0*banomcounts)
#            self.fmin=1.0
#            self.fanom=1.0
#            self.fanom=interp(self.fracz_fanom, numpy.array([0.8, 0.9, 1.0, 1.1, 1.2])*self.fanom, self.fz)
#            if self.fanom<0:
#                self.fanom=0
#            if self.fanom is None:
#                print "INTERPOLATION ERROR getting intial fanom"
#                self.fanom=1.0
#            while (self.btot_gen(self.fmin+delfmin, self.fanom-delfanom)>self.data).sum() < (self.btot_gen(self.fmin, self.fanom)>self.data).sum():
#                self.fmin+=delfmin
#                self.fanom-=delfanom
#                trylist=numpy.array(range(4))*self.fp+1
#                temp=interp(self.fracz_fanom, trylist*self.fanom, self.fz)
#                if temp is None:
#                    print "INTERPOLATION ERROR increasing fanom:", trylist
#                else:
#                    self.fanom=temp
#    #self.bimap, self.bqgrid, self.fmin, self.fanom,self.banom ready to be read
#        totbcknd=(self.fmin*self.bmin+self.fanom*self.banom)*self.killmap
#        self.data*=self.killmap
#        a=self.data<totbcknd
#        self.fracz=a.sum()/(1.0*self.killmap.sum())
#
#
#    def fracz_fanom(self, fanom):
#        return ((self.btot_gen(self.fmin, fanom)>self.data).sum())/numpy.float32(self.numpix)
#
#    def bqmin_gen(self, slotnum):
#        a=self.bdata[self.bimap==slotnum]
#        a.sort()
#        if a.size==0:
#            return 0
#        else:
#            return a[numpy.uint16(a.size*self.fz)]
#
#    def banom_gen(self):
#        temp=numpy.array([[self.banom_int((i-self.center[1])**2+(j-self.center[0])**2)[0]  for i in range(3450/self.bin)]  for j in range(3450/self.bin)], dtype='int32')*self.killmap
#        temp[temp<0]=0
#        return numpy.uint16(temp)
#
#    def btot_gen(self, fmin, fanom):
#        return self.bmin*fmin+self.banom*fanom

class fitfcns:
    #.finalparams .sigmas .parnames useful, returns fitfcn(x)
    def genfit(self, fcn, initparams, datatuple, markstr='unspecified', parnames=[], interaction=0,  maxfev=2000, weights=None):
        self.maxfev=maxfev
        self.performfit=True
        self.initparams=initparams
        self.sigmas=scipy.zeros(len(initparams))
        self.parnames=parnames
        self.finalparams=initparams
        self.error=False
        if weights is None:
            def wts(x):
                return 1
        elif weights=='parabolic':
            a=(datatuple[0][0]+datatuple[0][-1])/2.0
            b=(datatuple[0][-1]-datatuple[0][0])/2.0
            def wts(x):
                return 1.0+((x-a)/b)**2

        def res1(p, x1, y):
            return (y-fcn(p, x1))*wts(x1)

        def res2(p, x1,x2,y):
            return y-fcn(p, x1, x2)

        def res3(p, x1,x2,x3, y):
            return y-fcn(p, x1, x2, x3)

        def res4(p, x1,x2,x3,x4,  y):
            return y-fcn(p, x1, x2, x3, x4)

        resdic={1:res1,  2:res2,  3:res3,  4:res4}

        i=0
        for arr in datatuple:  #if the numerical data is given as a list or tuple then convert to arrays. regardless convert to float64 because leastsq REQUIRES THIS
            datatuple=datatuple[0:i]+tuple([numpy.float64(arr)])+datatuple[i+1:]
            i=i+1
        while self.performfit:
            fitout = scipy.optimize.leastsq(resdic[len(datatuple)-1],self.initparams, args=datatuple, maxfev=self.maxfev, full_output=1, warning=False)
            self.performfit=False

            if fitout[4]!=1:
                print 'Fitting Error at ', markstr,': ', fitout[3]
                self.error=True
            else:
                self.finalparams=fitout[0]
                self.covmat=fitout[1]
                self.sigmas=scipy.array([self.covmat[i, i] for i in range(len(self.sigmas))])

        def fitfcn(x):
            return fcn(self.finalparams, x)
        return fitfcn

    def poly(self, p, x):#both must be numpy arrays
        return numpy.array([p[i]*(x**i) for i in range(p.size)]).sum(0)

    def polyfit(self, datatuple, initparams, markstr='unspecified', interaction=0,  maxfev=2000, weights=None):
        #initparams can be an array of coefficients [constant,lin term, quad term,...] or an integer indicating the order of the polynomial
        if isinstance(initparams, int):
            initparams=numpy.ones(initparams+1)
        else:
            initparams=numpy.float32(initparams)
        parnames=[]
        i=0
        for par in initparams:
            parnames+=[''.join(('coef', `i`))]
            i+=1

        return self.genfit(self.poly, initparams, datatuple, markstr, parnames, interaction, maxfev, weights=weights)


    def gaussianfit(self, datatuple, initparams=scipy.array([1, 0, 1]), markstr='unspecified', interaction=0, showplot=True, maxfev=2000, weights=None):
        return self.genfit(self.Gaussian, initparams, datatuple, markstr, parnames=['coef', 'center', 'sigma'], interaction=interaction, maxfev=maxfev, weights=weights)

    def gaussian(self, p, x):
        return p[0]*scipy.exp(-0.5*((x-p[1])/p[2])**2)

    def lorentzianfit(self, datatuple, initparams=scipy.array([1, 0, 1]), markstr='unspecified', interaction=0, showplot=True, maxfev=2000, weights=None):
        return self.genfit(self, self.Lorentzian, initparams, datatuple, markstr, parnames=['coef', 'center', 'gamma'], interaction=interaction, maxfev=maxfev, weights=weights)

    def lorentzian(self, p, x):
        return (p[0]/scipy.pi)*p[2]/((x-p[1])**2+p[2]**2)


def hannsmooth(x, window):
    side=window//2
    s=numpy.r_[2*x[0]-x[side-1:0:-1],x,2*x[-1]-x[-2:-1*side-1:-1]]
    win=numpy.hanning(2*side+1)
    win/=win.sum()
    return numpy.convolve(win,s,mode='same')[side-1:1-side]

def savgolsmooth(x, window, order = 4, dx=1.0, deriv=0): #based on scipy cookbook
    side=numpy.uint16(window//2)
    s=numpy.r_[2*x[0]-x[side:0:-1],x,2*x[-1]-x[-2:-1*side-2:-1]]
    # a second order polynomal has 3 coefficients
    b = numpy.mat([[k**i for i in range(order+1)] for k in range(-1*side, side+1)])
    m = numpy.linalg.pinv(b).A[deriv] #this gives the dth ? of the base array (.A) of the pseudoinverse of b

    # precompute the offset values for better performance
    offsets = range(-1*side, side+1)
    offset_data = zip(offsets, m)

    smooth_data = list()
    for i in xrange(side, len(s) - side):
            value = 0.0
            for offset, weight in offset_data:
                value += weight * s[i + offset]
            smooth_data.append(value)
    return numpy.array(smooth_data)/(dx**deriv)

def wellspacedgrid(numpts, yvals=False): #numpts must be a perfect square
    sn=numpy.sqrt(numpts)
    temp=numpy.r_[numpy.array(range(numpts-1))*sn/(numpts-1.0)%1, 1]
    temp=temp.reshape((sn, sn))
    temp2=copy.copy(temp)
    for k in range(numpy.uint16(sn//4)):
        temp[2*k+1, :]=temp2[-2*k-2, :]
        temp[-2*k-2, :]=temp2[2*k+1, :]
    xvals=temp.flatten()
    if yvals:
        temp3=numpy.array(numpy.array(range(sn)))/(sn-1)
        temp4=numpy.zeros(sn)
        return(xvals, numpy.add.outer(temp3, temp4).flatten())
    else:
        return xvals


def bckndmincurve(allqvals, allivals, delq=None,  maxcurv=16.2, derivatepoints=5): #maxcurv is the maximum negative curvature in real units
    derside=derivatepoints//2
    dq=1.0*(allqvals[1]-allqvals[0])
    numq=allqvals.size
    if delq is None:
        qvals=allqvals
        ivals=allivals
        dindex=1
    else:
        dindex=numpy.uint16(numpy.round(delq/dq))
        qvals=allqvals[0:numq:dindex]
        ivals=allivals[0:numq:dindex]
        dq*=dindex
        numq=qvals.size
    dcurv=maxcurv/10.0 #this is how much curvature can be added to a given point in any one move
    dcurvfin=maxcurv/2.0
    winside_iter=2**numpy.array(range(numpy.uint16(numpy.log2(numq/2)//1),-2,-1))
    bvals=numpy.zeros(qvals.size)
    count=0
    for winside in winside_iter:
        if winside==0:
            qindpts=numpy.array(range(numq)) #qindpts is the center values where pixels will ba added
        else:
            qindpts=numpy.uint16(range(0, numq, 2*winside))
        windowlen=winside*2+1
        if winside<2:
            if dindex>1:
                winside=1
                window=numpy.array([0, dcurvfin*12.0*dq**2/30, 0])
            else:
                winside=0
                window=numpy.array([dcurvfin*12.0*dq**2/30])
        else:
            windowpeak=dcurv*((windowlen-1.0)*dq)**2/(19.74) #the 19.74 is for hanning window
            window=numpy.hanning(windowlen)*windowpeak
        repeat=True
        count=0
        firstqint=qindpts[1]-qindpts[0]
        while repeat:
            qindpts+=numpy.uint16(((firstqint*count/numpy.pi)%firstqint)//1)
            qindpts%=(numq-1)
            count+=1
            repeat=False
            for pt in qindpts:
                ind_2=pt-winside-derside
                if ind_2<0:
                    ind_2=0
                ind_1=pt-winside
                if ind_1<0:
                    ind_1=0
                ind1=pt+winside+1
                if ind1>numq:
                    ind1=numq
                ind2=pt+winside+derside+1
                if ind2>numq:
                    ind2=numq
                if (ind2-ind_2)<(2*derside+1):
                    if ind_2==0:
                        ind2+=derside
                    else:
                        ind_2-=derside
                a=winside-(pt-ind_1)
                b=winside+(ind1-pt)
                winsub=copy.copy(window)
                winsub=winsub[a:b]
                winfill_=numpy.zeros(ind_1-ind_2)
                winfill=numpy.zeros(ind2-ind1)
                redfrac=1
                if dindex>1: #this if is to make sure no ivals get zeroed in between bcknd points
                    newb=bvals[ind_1:ind1]+winsub
                    interpbwinsub=numpy.multiply.outer(winsub,numpy.array(range(dindex,0,-1))/(1.0*dindex)).flatten()[:1-dindex]+numpy.append(numpy.multiply.outer(winsub[1:],numpy.array(range(dindex))/(1.0*dindex)).flatten(),0)
                    interpnewb=numpy.multiply.outer(newb,numpy.array(range(dindex,0,-1))/(1.0*dindex)).flatten()[:1-dindex]+numpy.append(numpy.multiply.outer(newb[1:],numpy.array(range(dindex))/(1.0*dindex)).flatten(),0)
                    ivalscompare=allivals[ind_1*dindex:ind_1*dindex+interpnewb.size]
                    if (ivalscompare<interpnewb).sum()>0:
                        redfrac=(1.0-numpy.max((interpnewb-ivalscompare)/interpbwinsub))
                else:
                    if (ivals[ind_1:ind1]<(bvals[ind_1:ind1]+winsub)).sum()>0:
                        redfrac=(1.0-numpy.max(((bvals[ind_1:ind1]+winsub)-ivals[ind_1:ind1])/winsub))
                if redfrac>0.1:
                    winsub*=redfrac
                    if numpy.min(secder(bvals[ind_2:ind2]+numpy.r_[winfill_, winsub, winfill], dq))>-maxcurv:
                        bvals[ind_1:ind1]+=winsub
                        repeat=True
    if not allqvals[-1] in qvals:
        qvals=numpy.append(qvals, allqvals[-1])
        bvals=numpy.append(bvals, allivals[-1])
    else:
        qvals[-1]=allqvals[-1]
        bvals[-1]=allivals[-1]
    if allqvals.size!=qvals.size:
        binterpolator=scipy.interpolate.UnivariateSpline(qvals, bvals)
        bvals=binterpolator(allqvals)
    return bvals


def bcknd1dprogram(qgrid, ivals, attrdictORangles=None, smoothqwindow=0.5, cubiccritfrac=[.3, .3, .3,  .3],  maxcurvqinterval=0.4, maxcurv=16.2, returnall=False):
    #cubiccritfrac is the fraction of points above the cubic bcknd fit are removed from the next fit
    #critfrac is the fraction of points above the bcknd fit are removed from the next fit, the length gives the number of fit iterations
    #attrdictORtuple : can be attrdict and if not then an array of powdersolidangle values same length as qvals
    qvals=q_qgrid_ind(qgrid)
    notnaninds=numpy.where(numpy.logical_not(numpy.isnan(ivals)))
    qvals=qvals[notnaninds]
    ivals=ivals[notnaninds]

    if not isinstance(cubiccritfrac, list):
        cubiccritfrac=[cubiccritfrac, cubiccritfrac, cubiccritfrac, cubiccritfrac]  #if user sends just the critical fraction then default to 4 iterations using that fraction
    if isinstance(attrdictORangles, dict):
        L=attrdictORangles['cal'][2]
        wl=attrdictORangles['wavelength']
        angles=powdersolidangle_q(qvals, L, wl) #don't send a psize, use default 0.1mm
    elif isinstance(attrdictORangles, numpy.ndarray):
        angles=attrdictORangles
    else:
        angles=numpy.ones(ivals.shape, dtype='float32')
    fraczeroed=0.0
    dq=qgrid[1]
    smwin=(1.0*smoothqwindow/dq//2)*2+1
    qv=qvals
    iv=ivals/angles
    qv_0=qv[:]
    iv_0=iv[:]

    def fitfcn(x):
        return 50.0+5.0*x-0.04*(x**2)

    bfit=numpy.zeros(len(qv), dtype='float32')
    for cf in cubiccritfrac:
        fit=fitfcns()
        fitfcn=fit.polyfit((qv, iv), [fitfcn(0), (4.0*fitfcn(1.0)-fitfcn(2.0))/2.0, (fitfcn(2.0)-fitfcn(1.0))/2.0])
        if fit.error:
            break

        frachigh=(iv-fitfcn(qv))/fitfcn(qv)
        frachighcritval=numpy.sort(frachigh)[(1-cf)*frachigh.size//1]
        qv=qv[frachigh<frachighcritval]
        iv=iv[frachigh<frachighcritval]
        if not qv_0[-1] in qv:
            qv=numpy.append(qv, qv_0[-1])
            iv=numpy.append(iv, iv_0[-1])
        if not qv_0[0] in qv:
            qv=numpy.append(qv_0[0], qv)
            iv=numpy.append(iv_0[0], iv)
        bfit=fitfcn(qv_0)

    bfit[bfit<0]=0
    numzeroed=fraczeroed*qv_0.size
    count=0
    while numpy.array(bfit>iv_0).sum()>numzeroed:
        bfit*=0.98
        count+=1
        if count>1000:
            bfit=0.0*bfit
            break

    iv_1=iv_0-bfit
    iv_2=savgolsmooth(iv_1, smwin, order=4, deriv=0)
    iv_2[iv_2<0]=0
    bvals=bckndmincurve(qv_0, iv_2, delq=maxcurvqinterval, maxcurv=maxcurv)

    iv_3=iv_2-bvals
    iv_3[iv_3<0]=0

    if returnall:
        return (iv_3, iv_2, iv_1, iv_0,bvals, bfit, angles, notnaninds)
    else:
        ireturn=numpy.ones(qgrid[2], dtype='float32')*numpy.nan
        print iv_3.shape, ireturn.shape, len(notnaninds[0])
        ireturn[notnaninds]=numpy.float32(iv_3)[:]
        return ireturn

def qqnorm_gen(qq, critcounts=1.0):
    qqnorm=numpy.zeros(qq.shape, dtype=numpy.float32)
    qq[qq<critcounts]=0.0
    #return numpy.array([[qq[i, j]/numpy.sqrt(qq[i, i]*qq[j, j]) for j in range(qq.shape[1]) if qq[i, i]*qq[j, j]>0] for i in range(qq.shape[0])])
    size=qq.shape[0]
    diagarr=numpy.array([numpy.ones(size)*qq[i, i] for i in range(size)])
    indeces=qq*diagarr*diagarr.T>0
    qqnorm[indeces]=qq[indeces]/numpy.sqrt(diagarr[indeces]*diagarr.T[indeces])
    return qqnorm

def arrayzeroind2d(arr): #finds the indeces where the surface of array values is zero near those indeces, excluding exterior indeces - if arr is a list or tuple of arrays then has to be zero in all of them
    if isinstance(arr, numpy.ndarray):
        arr=[arr]
    elif isinstance(arr, tuple):
        arr=[arr[0]]
    neighsumsq=[]
    for A in arr:
        signarr=numpy.sign(A)
        siz=A.size #if they are not all the same size there will be an error
        neighsumsq.append((signarr[1:-1, 1:-1]+signarr[1:-1, 0:-2]+signarr[1:-1, 2:siz]+signarr[0:-2, 1:-1]+signarr[2:siz, 1:-1])**2)#sum of self plus 4 neighbors for the interior of the array
    s=''
    nss=neighsumsq
    for i in range(len(nss)):
        s=''.join((s, '(nss[', `i`, ']<25)&'))
    zeroind=numpy.where(eval(s[:-1]))
    return (zeroind[0]+1, zeroind[1]+1)#adding 1 to each part of the indeces tuple changes interior indecesd to full array indeces

def clustercoords_radius(coordlist, critdistsq): #takes a list (or array) of coords , i.e. [(1,2),(3,4)]and those within critical radius of each other, replaces them with the centroid of that group
    #assumes distance less than 10^5
    if len(coordlist)==0:
        print 'CANNOT CLUSTER EMPTY LIST OF POINTS'
        return numpy.array([])
    coordlist=numpy.array(coordlist)
    #print 'initial coords ', len(coordlist)
    sepsq=numpy.array([[(a[1]-b[1])**2.0+(a[0]-b[0])**2.0 for a in coordlist] for b in coordlist])#array where i,j is the distance between points indsepsq[i] and indsepsq[j]
    sepsqnozero=sepsq+numpy.eye(coordlist.shape[0], coordlist.shape[0])*10.0**10
    coordindclusters=[]
    coordstobeadded=[]
    while sepsqnozero.min()<critdistsq:
        temp=myargmin(sepsqnozero)
        ind1, ind2=temp//sepsq.shape[0],temp%sepsq.shape[0]#indeces such that the minimum separation is between coords indsepsq[ind1] and indsepsq[ind2]
        indgrp1=set(numpy.where(sepsq[ind1, :]<critdistsq)[0]) #this is all indeces that correspond to coords within critical radius of indsepsq[ind1], which will include the zero separation of ind1
        indgrp2=set(numpy.where(sepsq[ind2, :]<critdistsq)[0])
        indgrp=indgrp1|indgrp2#union to get rid of duplicates. this union means we group together everthing within critical radius of either coords which "overestimates" the critical radius but avoid calculating a centroid that later must be combined with other coords
        grpcentroid=tuple(numpy.array([coordlist[i] for i in indgrp]).mean(axis=0))
        sepsqnozero[list(indgrp), :]=10.0**10
        sepsqnozero[:, list(indgrp) ]=10.0**10
        coordindclusters+=[list(indgrp)]
        coordstobeadded+=[grpcentroid]
    #at the end of the loop, coordstobeadded is a list of the cnetroids with each corresponding to a list in coordindclusters, which has the indeces of the coords in the original coordlist
    coordindtoberemoved=set([])
    for ls in coordindclusters:
        coordindtoberemoved=coordindtoberemoved|set(ls)
    individualcoords=list(coordlist[list(set(range(coordlist.shape[0]))-coordindtoberemoved), :])
    allcentroids=coordstobeadded+individualcoords
    coordclusters=[coordlist[indlist, :] for indlist in coordindclusters]
    coordclusters+=[[coord] for coord in individualcoords]
    #print 'after clustering ', len(allcentroids)
    return (allcentroids, coordclusters) #2d array, first index gives you the ith coordinate i.e. coordlist[0] is array(4,5) REMEMBER TO ROUND THE CENTROIDS IF YOU WANT INTEGERS

def maxwithincluster(arr, clusters, centroids,  border=0):
    #cluster is a list of lists of [x,y] indeces and for each list, centroid is the [x,y] of the centroid. if clusters are indeces, centroid need not eb integer
    xlen=arr.shape[0]
    ylen=arr.shape[1]
    maxcoords=[]
    for tup in zip(clusters, centroids):
        clust=tup[0]
        cent=tup[1]
        xcoords,  ycoords=numpy.array(clust).T
        xlow=numpy.uint16(max(0, min(xcoords)-border))
        xhigh=numpy.uint16(min(xlen, max(xcoords)+border+1))
        ylow=numpy.uint16(max(0, min(ycoords)-border))
        yhigh=numpy.uint16(min(ylen, max(ycoords)+border+1))
        maxval=arr[xlow:xhigh, ylow:yhigh].max()
        posns=numpy.where(arr[xlow:xhigh, ylow:yhigh]==maxval)
        mindistcent=myargmin(numpy.array([(cent[0]-xlow-posns[0][i])**2+(cent[1]-ylow-posns[1][i])**2 for i in range(len(posns[0]))]))
        maxcoords+=[[posns[0][mindistcent]+xlow, posns[1][mindistcent]+ylow]]
    temp=zip(*maxcoords) #this now gets the intesection of the point indeces but it is a list of tuples instead of a tuple of ndarrays
    return ((numpy.uint16(numpy.array(temp[0])), numpy.uint16(numpy.array(temp[1]))), maxcoords)
    #the sceond elements of the return tuple is the list of [x,y] list where the maximum value within the rectangle defined by the extermes of the cluster points+border is located. in the even of multiple coords with same max value, the one closest to the centroid is given. the first element is the same info except a tuple of xvalarray,yvalarray

def arraypeaksearch(arr, ciss=0.1, belowdiagonal=False, dx=1, critcurvature=0, critvalue=None): #return tuple of arrays with x,y coords where there is a positive peak
    qq_x=arrayder_x(arr, dx)  #don't worry about dx in the derivatives becuase they all cancel out or magnitude doesn't matter
    qq_y=arrayder_y(arr, dx)
    qq_xx=arrayder_xx(arr, dx)
    qq_yy=arrayder_yy(arr, dx)
    qq_xy=arrayder_xy(arr, dx)
    firstderind=arrayzeroind2d([qq_x, qq_y])
    secderind=numpy.where((qq_xx*qq_yy>(qq_xy)**2)&(qq_xx<critcurvature)&(qq_yy<critcurvature))
    firstderindset=set(zip(firstderind[0], firstderind[1]))
    secderindset=set(zip(secderind[0], secderind[1]))
    if critvalue is None:
        pklist=numpy.array(list(firstderindset&secderindset))
    else:
        valind=numpy.where(arr>critvalue)
        valset=set(zip(valind[0], valind[1]))
        pklist=numpy.array(list(firstderindset&secderindset&valset))
    if len(pklist)==0:
        print 'NO PEAKS FOUND'
        return None
    else:
        if belowdiagonal:
            pklist=pklist[pklist.T[0]>=pklist.T[1]-numpy.sqrt(ciss)]
        clustcoords=clustercoords_radius(pklist, ciss)
        temp=zip(*clustcoords[0]) #this now gets the intesection of the point indeces but it is a list of tuples instead of a tuple of ndarrays
        return ((numpy.uint16(numpy.round(numpy.array(temp[0]))), numpy.uint16(numpy.round(numpy.array(temp[1])))), numpy.round(clustcoords[0]), clustcoords[1])
        #returns cluster, 1st element is a cluster of 2 arrays, the x and y indeces of peaks, the ith x and ith y give the centroid of the ith list of indeces in the third element of the return cluster
        #the second element has the same information as the first but it is a array of an [x,y] array

def peakbounds(arr, peakcenters, maxHWHM, critfracofpeak=0.5):
    #take subsets of arr and perform Gaussian fitting. the rectangular subsets include a border of sigmaindlimit*sigmas around the starts centers
    #fits to gaussians with zero offset, that is at a few sigmas away from center, the value is zero and the value is bigger than zero at each starting center
    #assumes sigmas*sigmalimit > ctrdevlimit so that the limit on a coordinate is its start position +- ctrdevlim without worry this will go out of the fitarr rectangle
    xlen=arr.shape[0]
    ylen=arr.shape[1]
    peakcenterbounds=[]
    for coord in peakcenters:  #one gaussian for each coord
        xlow=numpy.uint16(max(0, coord[0]-maxHWHM))
        xhigh=numpy.uint16(min(xlen, coord[0]+maxHWHM+1))
        ylow=numpy.uint16(max(0, coord[1]-maxHWHM))
        yhigh=numpy.uint16(min(ylen, coord[1]+maxHWHM+1))
        critval=arr[coord[0], coord[1]]*critfracofpeak
        searchsig_x=arr[coord[0]:xlow:-1, coord[1]]
        searchsigx=arr[coord[0]:xhigh, coord[1]]
        searchsig_y=arr[coord[0], coord[1]:ylow:-1]
        searchsigy=arr[coord[0], coord[1]:yhigh]
        searcharrs=[searchsig_x, searchsigx, searchsig_y, searchsigy]
        #each of these arrays will be zero when the value drops below a third of the peak, this is roughly sigma indeces away from the center
        HWHM=[]
        HWHMbycritval=[]
        defaults=[xlow, xhigh-1, ylow, yhigh-1]
        startcoord=[coord[0], coord[0], coord[1], coord[1]]
        direction=[-1, 1, -1, 1]
        for ardef in zip(searcharrs, defaults, startcoord, direction):
            sar=ardef[0]
            temp=numpy.where(sar//critval==0)
            if len(sar)<3:
                dsar=numpy.zeros(len(sar))
            else:
                dsar=numpy.array([sar[i]<sar[i+1] and sar[i+1]<sar[i+2] for i in range(len(sar)-2)]+[sar[-2]<sar[-1]])
            temp2=numpy.where(dsar==1)
            if len(temp[0])==0: #the zero was not found before running into the end of the fitarray so go to max sigma
                HWHMbycritval+=[0]
                if len(temp2[0])==0: #the value keep decreasing but never get to below critical value
                    HWHM+=[ardef[1]]
                else:
                    HWHM+=[ardef[2]+ardef[3]*temp2[0][0]]
            else:
                selectind=temp[0][0]
                if len(temp2[0])>0:
                    selectind=min(temp[0][0], temp2[0][0])  #in the range looked at, the critical value is reached and valuyes start increasing, use whichever index comes first
                if selectind==temp[0][0]:
                    HWHMbycritval+=[1]
                else:
                    HWHMbycritval+=[0]
                HWHM+=[ardef[2]+ardef[3]*selectind]
        peakcenterbounds+=[list(coord)+HWHM+HWHMbycritval]
    return peakcenterbounds # each element is a list [xcenter,ycenter, x-,x+,y-,y+,boolx-,x+,y=,y+] where e.g. y+ is the index where the array has dropped below critfrac of value or started increasing or rwached end of array. the bools are a list of 4 0's or 1's, 1 if the sigma was determined by crossing the value vice default of due to increasing

def qqpeakdiagnostics(qq, qqnorm, peakcenterbounds):
    fullpeakinfo=[]
    for cs in peakcenterbounds:
        pk=qq[cs[0], cs[1]]
        qqrectangle=qq[cs[2]:cs[3]+1, cs[4]:cs[5]+1]
        s=qqrectangle.sum()
        normave=(qqnorm[cs[2]:cs[3]+1, cs[4]:cs[5]+1]*qqrectangle/s).sum()
        fullpeakinfo+=[(cs, [pk, s, normave])]
    return fullpeakinfo  #list each element is a tuple, first tuple element is from peakceneterbounds, second is a list of the peak value, integral of peak value over the rectangle, and the expected value of qqnorm using the qqarray rectangle as a probabiliy distribution.

def makegreyplotimage(arr, logcounts=True):
    if logcounts:
        minnonzero=arr[arr>0].min()
        arr[arr<=0]=minnonzero
        arr=numpy.log10(arr)
    maxcts=arr.max()
    mincts=arr.min()
    plotarr=numpy.array([[[1-(1.0*val-mincts)/(maxcts-mincts)]*3 for val in col] for col in arr]) #grayscale the counts
    return (plotarr, (mincts, maxcts))

def makeqqnormpeakplotimage(arr, qqpktuplist, logcounts=True):
    cenpix=3
    qqnormave=numpy.array([a[1][2] for a in qqpktuplist])
#    qqmin=qqnormave.min()
#    qqmax=qqnormave.max()
#    qqnormave=(1.0*qqnormave-qqmin)/(qqmax-qqmin)
    qqnacolor=numpy.array([numpy.ones(len(qqnormave)), qqnormave, numpy.zeros(len(qqnormave))]).T
    xcen=numpy.array([a[0][0] for a in qqpktuplist])
    ycen=numpy.array([a[0][1] for a in qqpktuplist])
    if logcounts:
        minnonzero=arr[arr>0].min()
        arr[arr<=0]=minnonzero
        arr=numpy.log10(arr)
    maxcts=arr.max()
    mincts=arr.min()
    plotarr=numpy.array([[[1-(1.0*val-mincts)/(maxcts-mincts)]*3 for val in col] for col in arr]) #grayscale the counts
    for cd in zip(xcen, ycen, qqnacolor):
        plotarr[cd[0], max(cd[1]-cenpix, 0):cd[1]+cenpix+1, :]=cd[2][:]#color the expected value of the qqnorm from blue to red
        plotarr[max(cd[0]-cenpix, 0):cd[0]+cenpix+1, cd[1], :]=cd[2][:]
    b=numpy.array([0.0, 0.0, 1.0])
    boxplotlistx=[[a[0][2], a[0][3], a[0][3], a[0][2], a[0][2]] for a in qqpktuplist]
    boxplotlisty=[[a[0][4], a[0][4], a[0][5], a[0][5], a[0][4]] for a in qqpktuplist]
    for cds in zip(boxplotlistx, boxplotlisty):
        plotarr[cds[0][0]:cds[0][1], cds[1][1], :]=numpy.array([b]*(cds[0][1]-cds[0][0]))
        plotarr[cds[0][2], cds[1][1]:cds[1][2], :]=numpy.array([b]*(cds[1][2]-cds[1][1]))
        plotarr[cds[0][3]:cds[0][2], cds[1][3], :]=numpy.array([b]*(cds[0][2]-cds[0][3]))
        plotarr[cds[0][4], cds[1][4]:cds[1][3], :]=numpy.array([b]*(cds[1][3]-cds[1][4]))
    return (plotarr, (mincts, maxcts))


def arrayzeroind1d(arr, postoneg=False):
    sarr=numpy.sign(arr)
    if postoneg:
        zeroind=numpy.where(sarr[:-1]>sarr[1:])[0]
    else:
        zeroind=numpy.where(sarr[:-1]*sarr[1:]<=0)[0]
    return (1.0*zeroind*arr[(zeroind+1,)]-(zeroind+1)*arr[(zeroind,)])/(arr[(zeroind+1,)]-arr[(zeroind,)]) #returns array of the floating point "index" linear interpolation between 2 indeces

def clustercoords1d(pkind, critqsepind):#results will be sorted
    pkind.sort()
    newpks=[]
    i=0
    while i <(len(pkind)-1):
        if (pkind[i+1]-pkind[i])<critqsepind:
            newpks+=[(pkind[i+1]+pkind[i])/2.0]
            i+=2
        else:
            newpks+=[pkind[i]]
            i+=1
    return newpks #not exactly centroid but close enough

def clustercoordsbymax1d(arr, pkind, critqsepind):#results will be sorted. wherever there are peak indeces too close together. the peak index next to the peak index with highest arr value gets removed
    pkind.sort()
    indindslow=numpy.where((pkind[1:]-pkind[:-1])<critqsepind)[0]
    indindshigh=indindslow+1
    while indindslow.size>0:
        maxindindindlow=myargmax(arr[pkind[(indindslow,)]])
        maxindindindhigh=myargmax(arr[pkind[(indindshigh,)]])
        if arr[pkind[indindslow[maxindindindlow]]]>arr[pkind[indindshigh[maxindindindhigh]]]:
            pkind=numpy.delete(pkind, indindshigh[maxindindindlow])
        else:
            pkind=numpy.delete(pkind, indindslow[maxindindindhigh])

        indindslow=numpy.where((pkind[1:]-pkind[:-1])<critqsepind)[0]
        indindshigh=indindslow+1
    return pkind


def peaksearch1d(innn, dx=.1, critcounts=10, critqsepind=5, critcurve=None, max_withincritsep=False): #dx is delta q for one index. zeros of the first derivative of inn are grouped together if within critsepind. only negative slope in the firstder is used so no secder is necessary unless specify a critical curvature in count nm^2
    ifirstder=firstder(innn, dx)
    zeroind=arrayzeroind1d(ifirstder, postoneg=True)
    temp=numpy.where(innn[(numpy.uint16(numpy.round(zeroind)),)]>critcounts)
    fullpkind=zeroind[temp]
    if fullpkind.size==0:
        return fullpkind
    if max_withincritsep:
        pkind=clustercoordsbymax1d(innn, numpy.uint16(numpy.round(fullpkind)), critqsepind)
    else:
        pkind=clustercoords1d(fullpkind, critqsepind)#these pk indeces are floating point!!!
    if critcurve is not None:
        isecder=secder(innn, dx)
        temp=numpy.where(isecder[(numpy.uint16(numpy.round(pkind)),)]<(-1*critcurve))
        pkind=numpy.array(pkind)[temp]
    pkind=list(pkind)
    pkind.reverse()#highest to smallest for pairing below
    return numpy.array(pkind, dtype=numpy.float32)

def qqindeces_innn(knnn, qgrid, qgrid_qq, qqpktuplist, qqsigmasep=3.0, qqindsep=None, qqanisoalloyfrac=(0.01, 0.05)): #if qqindsep is a string, will assume separation scales with given fraction of 1/q=frac of d. if absolute qq then indeces assumed to be in innn indeces, i.e. spaced by qgrid[1]
#the base units are indeces in the 1d spectra, ignore peaks outside of the index range or qq
    startind=(qgrid_qq[0]-qgrid[0])//qgrid[1] #assume this is positive, can'e build qq over a larger range than that available in innn
    indratio=qgrid_qq[1]//qgrid[1]
    endind=startind+(qgrid_qq[2]-1)*indratio #start and end indeces for the 1d images using the range of the qq analysis
    pkind=knnn[(knnn>startind)&(knnn<endind)]#throw away peak positions outside of the range used in qq
    def ind1d_ind2d(ind2d):
        returnnumber=False
        if isinstance(ind2d, float) or isinstance(ind2d, int):
            ind2d=list(ind2d)
            returnnumber=True
        ind2d=numpy.array(ind2d)
        ind1d=ind2d*indratio+startind
        if returnnumber:
            return ind1d[0]
        else:
            return list(ind1d)

#    qqpkinfosub=[]
#    origind_subind=[]
#    count=-1
#    for tup in zip(qqpks, qqpkinfo):
#        count+=1
#        if tup[1][2]>critqqnorm:
#            qqpkinfosub+=[tup] #pkinfosub now has both qqpks and qqpkinfo in it
#            origind_subind+=[count]#array indexed like qqpkinfosub with values equal to the index of the original qqpk arrays
    qqpkcenqqunits=[tup[0][0:2] for tup in qqpktuplist]

    qqpkcen=[ind1d_ind2d(tup[0][0:2]) for tup in qqpktuplist]
    qqsigs=[list(numpy.abs(numpy.int32(tup[0][2:6])-numpy.int32([tup[0][0]]*2+[tup[0][1]]*2))*indratio) for tup in qqpktuplist] #the*2 is to repeat x,x,y,y
    qqpkbools=numpy.array([tup[0][6:10] for tup in qqpktuplist])
    qqnorm=numpy.array([tup[1][2] for tup in qqpktuplist])
    qqpkvolume=numpy.array([tup[1][1] for tup in qqpktuplist])
    if not (qqindsep is None):
        qqcritsep=numpy.ones(range(len(pkind)), dtype=numpy.float32)*qqindsep #rememebr this is already in innn indeces
    else:
        alpha,beta=qqanisoalloyfrac
        qqx=numpy.array(q_qgrid_ind(qgrid_qq, numpy.array([cd[0] for cd in qqpkcen])))#DEAL WITH THE ACTUAL Q VALUES FOR THIS - may be more efficient way to do it
        qqy=numpy.array(q_qgrid_ind(qgrid_qq, numpy.array([cd[1] for cd in qqpkcen])))
        K=alpha**2*beta**2*qqx*qqy-alpha**4*(qqx**2+qqy**2+2.0*qqx*qqy)
        L=2*alpha**2*(qqx+qqy)
        r=-1.0*qqx*(beta**2*qqy-L)/(qqy*(beta**2*qqx-L))
        s=-0.25*(L**2-(2.0*alpha*beta*qqx)**2-(2.0*alpha*beta)**2*qqx*qqy+beta**4*qqx**2)/(beta**2*qqx**2*K)
        t=-0.25*(4*alpha**2-beta**2)/K
        AA=(t+s)*qgrid[1]**2
        BB=(t+r**2*s)*qgrid[1]**2
        CC=2*(t+r*s)*qgrid[1]**2
    unassignedpkindind=set(range(len(pkind))) #set of all indeces of pkind
    qq_innn_dicts=[]
    qqindsets_pkind=[set([]) for p in pkind]
    for qi in range(len(pkind)-1):
        for qj in range(qi+1, len(pkind)): #this assure qi!=qj, qi>qj
            qhigh=pkind[qi]
            qlow=pkind[qj]
            xqqsep=numpy.array([qhigh-cd[0] for cd in qqpkcen])
            yqqsep=numpy.array([qlow-cd[1] for cd in qqpkcen])
            xsigind=numpy.uint16([(numpy.sign(x)+1)//2 for x in xqqsep])
            ysigind=numpy.uint16([(numpy.sign(y)+1)//2+2 for y in yqqsep])
            qqwheresig=numpy.where(numpy.array([qqpkbools[i][xsigind[i]]+qqpkbools[i][ysigind[i]] for i in range(len(qqpkbools))])==2)#both bools for the respective x direction and y direction must have been determined by critical counts for a sigma measurement to be made

            xsig=numpy.array([qqsigs[i][xsigind[i]] for i in range(len(qqsigs))])
            ysig=numpy.array([qqsigs[i][ysigind[i]] for i in range(len(qqsigs))])
            xsig[xsig==0]=0.001#just to avoid div by zero
            ysig[ysig==0]=0.001

            insertqqind=numpy.zeros(len(qqpkbools))
            if not qqindsep is None:
                withindefaultlim=(xqqsep**2+yqqsep**2)<(qqcritsep[qi]*numpy.sqrt(xqqsep**2+yqqsep**2))
            else:
                withindefaultlim=(AA*xqqsep**2+BB*yqqsep**2+CC*numpy.abs(xqqsep*yqqsep))<1.0
            withinsiglim=(xqqsep**2/xsig+yqqsep**2/ysig)<(qqsigmasep*numpy.sqrt(xqqsep**2+yqqsep**2)) #the mathematical form is to wieght the sigma deviations by the dot products with the vector separation implied by x,yqqsep
            insertqqind=withindefaultlim
            insertqqind[qqwheresig]=withinsiglim[qqwheresig]
            indtoadd=numpy.where(insertqqind==True)[0]
            for ind in indtoadd:
                delsig=None
                delqind=None
                temp=numpy.sqrt(xqqsep[ind]**2+yqqsep[ind]**2)
                if ind in qqwheresig[0]:
                    if temp==0:
                        delsig=temp
                    else:
                        delsig=(xqqsep[ind]**2/xsig[ind]+yqqsep[ind]**2/ysig[ind])/temp
                else:
                    if temp==0:
                        delqind=temp
                    else:
                        delqind=(xqqsep[ind]**2+yqqsep[ind]**2)/temp
                qq_innn_dicts+=[{'qqpkind':ind, 'qqcenteriind':ind1d_ind2d(qqpkcenqqunits[ind]),'qqcenterqqind':qqpkcenqqunits[ind], 'qindhighlow':(qhigh, qlow), 'kindhighlow':(qi, qj),   'delsig':delsig,  'delqind':delqind,  'qqpkvolume':qqpkvolume[ind], 'qqpknorm':qqnorm[ind]}]#all indeces are in units of 1dint (and floating point) except for qqcenter
                unassignedpkindind-=set([qi, qj])
                qqindsets_pkind[qi]|=set([ind])
                qqindsets_pkind[qj]|=set([ind])
    unassignedpkind=[pkind[i] for i in unassignedpkindind]
    return (qq_innn_dicts,  qqindsets_pkind, unassignedpkind) #list: dictionary for every qqindex in innn,      list: for each  pkind, a set of the qqindeces that contain that  pkind,  set of pkind from innn that are not in any of the indeces


def outerlist_order_norepeat(tup1,tup2):
#    print tup1, '*', tup2
    return [tuple(min([t1, t2],[t2, t1])) for t1 in tup1 for t2 in tup2 if t1!=t2] #since knnn is ordered highest to lowest, we want everything to be order (a,b) where a<b so that ifnnn_a>ifnnn_b


def ktupphases_qqind(ktuplist, critnumipks=0):    #list of tuples (kindhigh,kindlow)
#    def numkinphase(phasetupset):
#        tempset=set([])
#        for tempi in phasetupset:#if there are a bunch of indeces in here but they all have the same qpk values..well only the number of unique qpk values counts
#            tempset|=set(tempi)
#        return len(tempset)
#    def numkinphasecmp(pa,pb):
#        return 1*(numkinphase(pa)>numkinphase(pb))-1*(numkinphase(pa)<numkinphase(pb))
    if critnumipks<=2:
        critnumtups=1
    else:
        critnumtups=(critnumipks)*(critnumipks-1)//2 # i.e. "n choose 2"
    def phasesizecmp(pa,pb):
        return 1*(len(pa)>len(pb))-1*(len(pa)<len(pb))
#    def crosstuplesthatexists(tup1, tup2):
#        return [crosstup for crosstup in outerlist_order_norepeat(tup1,tup2) if crosstup in qqpkind_ktupDICT.keys() ]
    def tuplistallexist(tuplist):
        return all([(tup1 in ktuplist) for tup1 in tuplist])
    phases=[]
    print 'ktups', len(ktuplist)
    for ktup in ktuplist:
        phases.sort(cmp=phasesizecmp) #puts the longest phases first
        if len(phases)%1==0:
            print 'phases', len(phases)
        for phs in phases: #phs is a pointer
#            print phs, ' in ', phases

            if not (ktup in phs):
                hypotheticalphase=set([ktup])|phs
                if sum([hypotheticalphase<=tempph for tempph in phases])==0: # if adding to this phases would not form a subset of an existing phase
                    crosstermtuplist=[]
                    for phsktup in phs:
                        crosstermtemp=outerlist_order_norepeat(phsktup, ktup) #list of lists of tups
                        if tuplistallexist(crosstermtemp):
                            crosstermtuplist+=crosstermtemp
                        else:
                            crosstermtemp=None
                            break
                    if not (crosstermtemp is None):
                        phases+=[copy.copy(phs)|set(crosstermtuplist)] #allows for subsets to exist in the building of phases to allow for branching of phases
        phases+=[set([ktup])]#always make the ktup its own phases so all subsequent ktups can possible be added to it - this means at the end there will be a phase for every ktup
    phases.sort(cmp=phasesizecmp, reverse=True)
    i=0
    while i<len(phases)-1:
        if len(phases[i])>=critnumtups:
            break
        else:
            del phases[i]
    while i<len(phases)-1:
        if any([phases[i]<=tempph for tempph in phases[i+1:]]): #is subset of any higher order phase
            del phases[i]
        else:
            i+=1
    return phases #list of phases, a phase is a set of tuples (kindhigh,kindlow)

def phasevecs_ktup(qqpkind_ktupDICT, kindtuplephases, qqpkindveclength, kindveclength, critnumqqpks):  #phase (qqpks set) can be instanced by different tuple sets and this repititon is reflected in the returned data
    qqpkind_ktupDICT
    def qqindlist_ktupset(ktupset):
        qqindset=set([])
        for ktup in ktupset:
            qqindset|=qqpkind_ktupDICT[ktup]
        if len(qqindset)<critnumqqpks:
            return [-1]

        return list(qqindset)

    def kind_ktupset(ktupset):
        tempset=set([])
        for ktup in ktupset:
            tempset|=set(ktup)
        return list(tempset)


    qqindlist_phase=map(qqindlist_ktupset, kindtuplephases)
    kindlist_phase=map(kind_ktupset, kindtuplephases)

    while [-1] in qqindlist_phase:
        del kindlist_phase[qqindlist_phase.index([-1])]
        qqindlist_phase.remove([-1])

    qqpkindvecindeces=numpy.uint16([[phasenum, qqind] for phasenum, qqindlist in enumerate(qqindlist_phase) for qqind in qqindlist]).T
    kindvecindeces=numpy.uint16([[phasenum, kind] for phasenum, kindlist in enumerate(kindlist_phase) for kind in kindlist]).T
    if len(qqindlist_phase)==0:
        return (None,  None)
    qqpkindphasevecs=numpy.zeros((len(qqindlist_phase), qqpkindveclength),  dtype=numpy.bool_)
    qqpkindphasevecs[(qqpkindvecindeces[0], qqpkindvecindeces[1])]=True
    kindphasevecs=numpy.zeros((len(qqindlist_phase), kindveclength),  dtype=numpy.bool_)
    kindphasevecs[(kindvecindeces[0], kindvecindeces[1])]=True
    return (qqpkindphasevecs, kindphasevecs)

def indexarr_xzgrid(xgrid, zgrid, pointlist=None):
    arr=numpy.reshape(numpy.int32(range(xgrid[2]*zgrid[2])), (xgrid[2], zgrid[2]))
    if pointlist is None:
        return arr
    else:
        kill=[[not (arr[i,j] in pointlist) for j in range(arr.shape[1])] for i in range(arr.shape[0])]
        arr[numpy.where(kill)]=-1
        return arr

def subsettest_boolarray(a, b): # 1 if a is a subset of b, -1 if b is a subset of a, 0 otherwise
    return int(not(numpy.any(a*(a^b))))-int(not(numpy.any(b*(a^b)))) #if a is a subset of b, the excluseive or elements will be in b so a*XOR will be all zeros
def spatialblobinfo_phase(samplebool_phase, xgrid, zgrid, pointlist, radius_xpts=1, minptsinblob=3):
    #on 7Feb2010: this function is probably not used anymore - if it is used, support must be added fro "USER-COMPILED' cases where xgrid,zgrid are meaningless
    #img_phase  index is the phase number, gives the set of img numbers that contain that phase
    spacingratio=zgrid[1]/xgrid[1]
    sampleindexarr=indexarr_xzgrid(xgrid, zgrid, pointlist)
    mask=sampleindexarr>-1
    phaseblobinfo=[]
    phasenum=-1
    for samplebool in samplebool_phase:
        phasenum+=1
        #phasemap=numpy.bool_([[imgindexarr[i,j] in imgset for j in range(imgindexarr.shape[1])] for i in range(imgindexarr.shape[0])])
        phasemap=numpy.reshape(samplebool, (xgrid[2], zgrid[2]))
        blobarr, blobneighfraclist = blobarrgen(phasemap, radius=radius_xpts, minptsinblob=minptsinblob, mask=mask, spacingratio=spacingratio)
        blobnum=0  #intnetionall start at 1 in loop
        for blobneighfrac in blobneighfraclist:
            blobnum+=1
            #phaseblobinfo+=[(phasenum, imgindexarr[numpy.where(blobarr==blobnum)], blobneighfrac)]
            phaseblobinfo+=[(phasenum, (blobarr==blobnum).flatten(), blobneighfrac)]
    return phaseblobinfo #list of tuples. each tuple is a phase,blob instance. the tuple is the index of the phase in the imgsets_phase array, the array of points in the blob (subset of pointlist), and the blob nieghbor fraction

def blobarrgen(arr, radius=1, minptsinblob=1, mask=None, spacingratio=1.0):
    """    Find connected regions in a binary image.
        If the image is not binary, then convert it to one
        using arr > arr.min() as a criteria.

        everything (e.g. radius) is in units of the spacing between x-(1st)indeces the z- or y- or 2nd index spacing is the x-spacing * spacingratio

        Parameters:
        arr:        a numpy array with two dimensions

        minptsinblob:    patches less than minptsinblob pixels
                will be rejected

                returns [NewImage,hitsI,hitsJ]
                where hitsI is a list of I indices
                and hitsJ that of J indices
        Newimage:    an image with confluent areas marked
                with the same number
                The maximum of this image is the number
                of areas found
    """

    if arr.ndim != 2 :
        print "2D arrays are required"
        return

    if mask is None:
        mask=numpy.ones[arr.shape]
    #If not a binary image, then convert to one:
    if arr.max() != 1 and arr.min() != 0:
        print "Not a binary image, converting to one:"
        arrtmp = (arr > arr.min())*mask
    else :
        arrtmp = arr*mask

    if arrtmp.sum < 2 :
        print "Empty image"
        return

    blobarr = numpy.zeros((arrtmp.shape),dtype=numpy.uint16)
    marker = 1
    blobneighfrac=[]
    #points that are eligible for blobs:
    nonzerocoords = arrtmp.nonzero()

    for (x,y) in zip(nonzerocoords[0],nonzerocoords[1]):
        if arrtmp[x,y] != 0 :
            ans = findsingleblob(arrtmp,x,y,radius, mask, spacingratio)
            blobx = numpy.asarray(ans[0])
            bloby = numpy.asarray(ans[1])
            if len(blobx) >= minptsinblob:
                blobneighfrac+=[ans[2]/(1.0*ans[2]+ans[3])] #this will only div by zero if these was a point that had no neighbors within mask
                blobarr[blobx,bloby] = marker
                marker = marker + 1
            #zero the blob:
            arrtmp[blobx, bloby] = 0
    return (blobarr, blobneighfrac) #0 where there is no blob, integer deonting a blob. blobs cannot overlap


def findsingleblob(arr, x, y, radius=1, mask=None, spacingratio=1.0):
    """     take a binary image, and if (x,y) is a nonzero pixel,
        return a list of coordinates of the confluent area this
        pixel is within.

        everything (e.g. radius) is in units of the spacing between x-(1st)indeces the z- or y- or 2nd index spacing is the x-spacing * spacingratio

        Based on the code from Eric S. Raymond posted to:
        http://mail.python.org/pipermail/image-sig/2005-September/003559.html

        Parameters:
        arr :        a binary image
        x,y:        start coordinates

        Return:
          [I,J]        a list of indices
"""
    Ni,Nj = arr.shape
    if mask is None:
        mask=numpy.ones[arr.shape]
    arrcopy=copy.copy(arr)
    edge = [[x,y]]
    bloblist_x = [x]
    bloblist_y = [y]
    numneighlinks=0
    numneighnolink=0

    rng=range(-numpy.int16(numpy.floor(radius)),numpy.int16(numpy.floor(radius))+1)
    xdevs=numpy.int16(numpy.outer(rng,numpy.ones(len(rng))).flatten())
    ydevs=numpy.array(rng*len(rng))
    loc=numpy.where(xdevs**2+(spacingratio*ydevs)**2<=radius**2)
    xdevs=xdevs[loc]
    ydevs=ydevs[loc]
    numneigh=len(xdevs)-1
    while edge:
        newedge = []
        #Check all pixels:
        for (x,y) in edge:
            neighlist=zip(list(x+xdevs),list(y+ydevs))
            neighlist.remove((x,y))#remove the position of interest because it should not count as its own neighbor
            arrcopy[x, y]=0
            for (i,j) in neighlist :
                #protect for out of range indices:
                if i < 0 or j < 0 or i >= Ni or j >= Nj :
                    continue
                elif mask[i, j]:
                    if arrcopy[i,j]:
                        arrcopy[i,j] = 0
                        #store the point to further examination
                        newedge.append((i,j))
                        #add it to the blob
                        bloblist_x.append(i)
                        bloblist_y.append(j)

                    #look at original image to see if this neighbor has same +1 value
                    if arr[i,j]:
                        numneighlinks+=1
                    else:
                        numneighnolink+=1
        edge = newedge
    #End of check all points (while)
    return [bloblist_x, bloblist_y, numneighlinks, numneighnolink, numneigh]
    #len(bloblist_x) is the number of points in the blob
    #numneighlinks is twice the number of links due to double counting
    #numneighnolink is comparable to numneighlinks
    #numneighs*numneighlinks/(numneighlinks+numneighnolink) is the average value for number of neighbors with same +1 value
    #len(bloblist_x)*numneighs+(numneighlinks+numneighnolink) is the number of times a neighbor was outside of mask

def flatten(x):
    result = []
    for el in x:
        if isinstance(el, (list, tuple)):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

def peakinfo_pksavearr(peaks, fiterr=False, removebeyondqgrid=None):
    inds=numpy.logical_not(numpy.isnan(peaks[0, :]))
    if not removebeyondqgrid is None:
        a, b, c=minmaxint_qgrid(removebeyondqgrid)
        qvals=peaks[0, inds]
        inds=inds[(qvals>a)&(qvals<b)]
    if fiterr:
        return peaks[0, inds], peaks[1, inds], peaks[2, inds], peaks[3, inds], peaks[4, inds], peaks[5, inds]
    else:
        return peaks[0, inds], peaks[1, inds], peaks[2, inds]

def waveletset1d(qgrid, qscalegrid, qposngrid):
#    return numpy.float32([[[1.64795*(1.0-((q-qp)/qs)**2)*numpy.exp(-0.5*((q-qp)/qs)**2)/numpy.sqrt(2.0*numpy.pi*qs) for q in q_qgrid_ind(qgrid)] for qp in q_qgrid_ind(qposngrid)] for qs in scale_scalegrid_ind(qscalegrid)])
    ans=[]
    for qs in scale_scalegrid_ind(qscalegrid):
        ans+=[numpy.float32([[1.64795*(1.0-((q-qp)/qs)**2)*numpy.exp(-0.5*((q-qp)/qs)**2)/numpy.sqrt(2.0*numpy.pi*qs) for q in q_qgrid_ind(qgrid)] for qp in q_qgrid_ind(qposngrid)])]
    return numpy.float32(ans)

def wave1dkillfix(wave, targetenergy, dq=1):
    plist=numpy.where(wave>0)
    nlist=numpy.where(wave<0)
    wavep=wave[plist]
    waven=wave[nlist]
    sump=wavep.sum()
    sumn=-1.0*waven.sum()
    enp=((dq*wavep)**2).sum()
    enn=((dq*waven)**2).sum()
    f=numpy.sqrt(targetenergy/(enp+((sump/sumn)**2)*enn))
    wave[plist]*=f
    wave[nlist]*=(f*sump/sumn)
    return wave

def perform_ridges_wavetrans1d(wtrev, qsindlist, noiselevel, numscalesskippedinaridge=1.5):# the scale index of the wt has been reversed so that this fucntion steps from biggest to msallest wavelet scale. So the scale index of ridges is inverted from that of the previously saved wt

    initpeakind=list(numpy.int16(numpy.round(peaksearch1d(wtrev[0], dx=1, critcounts=noiselevel, critqsepind=qsindlist[0], max_withincritsep=True))))#this dx no good if using curvature
    ridges=[[ind]+[32767]*(wtrev.shape[0]-1) for ind in initpeakind]

    for scalecount in range(1, wtrev.shape[0]):
        wtrow=wtrev[scalecount, :]
        peakind=list(numpy.int16(numpy.round(peaksearch1d(wtrow, dx=1, critcounts=noiselevel, critqsepind=qsindlist[scalecount], max_withincritsep=True))))
        for ridgecount, ridge in enumerate(ridges):
            if len(peakind)>0 and ridge[scalecount]==32767: #need peaks to assign and also if ridge forked in previous scale then that ridge has ended
                temp=1
                while ridge[scalecount-temp]==32767 or ridge[scalecount-temp]<0:
                    temp+=1
                if temp-1<=numscalesskippedinaridge:
                    ridgerep=ridge[scalecount-temp]
#                    print 'PEAKIND', peakind
#                    print scalecount, 'RIDGE', ridge
#                    print 'ridgerep', ridgerep
#                    print 'critsep**2', (1.5*qsindlist[scalecount-1])**2
#                    print 'sep**2', (1.0*numpy.float32(peakind)-ridgerep)**2
                    closeenoughinds=list(numpy.where((1.0*numpy.float32(peakind)-ridgerep)**2<(1.5*qsindlist[scalecount-1])**2)[0])#the 1.3 loosens the contraint for associating a current peak with one from the previous (larger) qscale and thus makes mother->children associations more common
                    #print 'closeenoughinds1', closeenoughinds
                    allridgereps=numpy.float32([r[scalecount-temp] for r in ridges])
                    closeenoughinds=[ceind for ceind in closeenoughinds if ridgecount==myargmin((peakind[ceind]-allridgereps)**2)]#peaks are only close enough to a ridge if that ridge is the closest tot he peak
                    closestind=myargmin((numpy.float32(peakind)-ridgerep)**2)
                    if len(closeenoughinds)==1:
                        ridge[scalecount]=peakind.pop(closestind)
                    elif len(closeenoughinds)>1:
                        newridgestart=numpy.int16(ridge[:scalecount])
                        newridgestart[newridgestart!=32767]=-1*ridgecount-1
                        newridgestart=list(newridgestart)
                        closeenoughinds.sort(reverse=True) #this is imperative because otherwise the .pop() will mess things up
                        for ceind in closeenoughinds:
                            pkind=peakind.pop(ceind)
                            ridges+=[newridgestart+[pkind]+[32767]*(wtrev.shape[0]-scalecount-1)]
                            if ceind==closestind:
                                ridges[ridgecount]=ridge[:scalecount]+[-1*(len(ridges)-1)-1]*(len(ridge)-scalecount) #the forked ridge is fille dwith the ridge index of its closest new subridge

        for pkind in peakind:
            ridges+=[[32767]*scalecount+[pkind]+[32767]*(wtrev.shape[0]-scalecount-1)]

    return ridges

#COPIED 12Jan2010
#def perform_ridges_wavetrans1d(wtrev, qsindlist, noiselevel, numscalesskippedinaridge=1.5):
#
#    initpeakind=list(numpy.int16(numpy.round(peaksearch1d(wtrev[0], dx=1, critcounts=noiselevel, critqsepind=qsindlist[0], max_withincritsep=True))))#this dx no good if using curvature
#    ridges=[[ind]+[32767]*(wtrev.shape[0]-1) for ind in initpeakind]
#
#    for scalecount in range(1, wtrev.shape[0]):
#        wtrow=wtrev[scalecount, :]
#        peakind=list(numpy.int16(numpy.round(peaksearch1d(wtrow, dx=1, critcounts=noiselevel, critqsepind=qsindlist[scalecount], max_withincritsep=True))))
#        for ridgecount, ridge in enumerate(ridges):
#            if len(peakind)>0 and ridge[scalecount]==32767: #need peaks to assign and also if ridge forked in previous scale then that ridge has ended
#                temp=1
#                while ridge[scalecount-temp]==32767 or ridge[scalecount-temp]<0:
#                    temp+=1
#                if temp-1<=numscalesskippedinaridge:
#                    ridgerep=ridge[scalecount-temp]
#                    closeenoughinds=list(numpy.where((1.0*numpy.float32(peakind)-ridgerep)**2<1.0*qsindlist[scalecount-1]**2)[0])
#                    closestind=myargmin((numpy.float32(peakind)-ridgerep)**2)
#                    if len(closeenoughinds)==1:
#                        ridge[scalecount]=peakind.pop(closestind)
#                    elif len(closeenoughinds)>1:
#                        newridgestart=numpy.int16(ridge[:scalecount])
#                        newridgestart[newridgestart!=32767]=-1*ridgecount-1
#                        newridgestart=list(newridgestart)
#                        closeenoughinds.sort(reverse=True) #this is imperative because otherwise the .pop() will mess things up
#                        for ceind in closeenoughinds:
#                            if ceind==closestind:
#                                ridges[ridgecount]=ridge[:scalecount]+[-1*(len(ridges)-1)-1]*(len(ridge)-scalecount) #the forked ridge is fille dwith the ridge index of its closest new subridge
#                            pkind=peakind.pop(ceind)
#                            ridges+=[newridgestart+[pkind]+[32767]*(wtrev.shape[0]-scalecount-1)]
#
#
#        for pkind in peakind:
#            ridges+=[[32767]*scalecount+[pkind]+[32767]*(wtrev.shape[0]-scalecount-1)]
#    return ridges
#
#def perform_peaks_ridges1d(wt, ridges, ridgescalecritind=0, minridgelength=3):
#    ridgeinds=numpy.where(((ridges!=32767).sum(axis=1)>=minridgelength)&(ridges[:, -1]!=32767))[0] #this is the ridge length including the "good" ridge components from other ridges associated through forking that has to be at least minridgelength but this is only good if the ridge goes to the smallest scale
#    ridgeinds2=numpy.where(((ridges!=32767)*(ridges>=0)).sum(axis=1)>=minridgelength)[0]#this will catch the ridges that don't go to the end but are long enough on their own (not counting mother forks). mother forks ruled out later
#    ridgeinds=numpy.array(list(set(ridgeinds)|set(ridgeinds2)))
#    peaks=[]#list of [peak scaleind, posnind]
#    if len(ridgeinds)==0:
#        print 'no valid ridges'
#        return []
#    for ridge in ridges[ridgeinds]:
#        rind=numpy.where(ridge!=32767)[0]
#        if ridge[rind[-1]]>=0: #if this fails that means the ridge was forked and thus its peaks will be found in other ridges
#            rind=numpy.where((ridge!=32767)&(ridge>=0))[0] #this will generally be a continuous sequence of indeces except for possibler holes of size numscalesskippedinaridge
#            wtvals=(wt[(wt.shape[0]-1-rind, ridge[rind])]) #-rind inverts but resulting order is still that of rind
#            indforincreasingtest=(rind>=ridgescalecritind)
#            if (wtvals[indforincreasingtest][1:]>wtvals[indforincreasingtest][:-1]).sum()>0: #if a ridge wt value is bigger than its predecessor(larger scale) then the wt isn't strictly increasing with increasing qscale
#                scaleind=(wt.shape[0]-1-rind[myargmax(wtvals[indforincreasingtest])]) #choose the wt scale and posn at the local maximum with largest wt
#                posnind=ridge[rind[-1]]
#                peaks+=[[scaleind, posnind]]
#    return peaks
#
#
def perform_peaks_ridges1d(wt, ridges, ridgescalecritind=0, minridgelength=1, minchildlength=1, minridgewtsum=0., minchildwtsum=0., verbose=False):#wt scale ind is small->big but ridges is big->small and ridgescalecritind is of ridges
    ridgeinds=numpy.where(((ridges!=32767).sum(axis=1)>=minridgelength)&(ridges[:, -1]!=32767))[0] #this is the ridge length including the "good" ridge components from other ridges associated through forking that has to be at least minridgelength but this is only good if the ridge goes to the smallest scale
    ridgeinds2=numpy.where(((ridges!=32767)*(ridges>=0)).sum(axis=1)>=minridgelength)[0]#this will catch the ridges that don't go to the end but are long enough on their own (not counting mother forks). mother forks ruled out later
    ridgeinds=numpy.array(list(set(ridgeinds)|set(ridgeinds2)))
    if verbose:
        print 'ridge inds passed length tests: ', ridgeinds
        print ridges
    peaks=[]#list of [peak scaleind, posnind]
    mother_peaks=[] # every element is a tuple, the 1st elemnt is like an entry of peaks, the 2nd is a list of the children
    ridgeind_peaks=[]
    for count, ridge in enumerate(ridges):
        rind=numpy.where(ridge!=32767)[0]

        if len(rind)>0: #if this fails that means the ridge is essentially empty
            motherbool=ridge[rind[-1]]<0
            if verbose:
                if motherbool:
                    tempstr='(MOTHER) '
                else:
                    tempstr=''
                print 'NEW RIDGE ', tempstr, count, ': ', ridge
                print 'length test:', len(rind)>0
            rind=numpy.where((ridge!=32767)&(ridge>=0))[0] #this will generally be a continuous sequence of indeces except for possibler holes of size numscalesskippedinaridge
            wtvals=(wt[(wt.shape[0]-1-rind, ridge[rind])]) #-rind inverts but resulting order is still that of rind. wtvals is now the select values from wt but ordered from big->small wavelet scale
            totridgewt=wtvals.sum()
            ridgelen=len(rind)
            motherind=motherridgeind_childridge(ridge)
            if not motherind is None:
                if verbose:
                    print 'tot wt of child test:', totridgewt, minchildwtsum, totridgewt>minchildwtsum
                if totridgewt<=minchildwtsum:
                    continue
                if verbose:
                    print 'length of child test:', ridgelen, minchildlength, ridgelen>=minchildlength
                if ridgelen<minchildlength:
                    continue
                mridge=ridges[motherind]
                mrind=numpy.where((mridge!=32767)&(mridge>=0))[0] #this will generally be a continuous sequence of indeces except for possibler holes of size numscalesskippedinaridge
                mwtvals=(wt[(wt.shape[0]-1-mrind, mridge[mrind])])
                if verbose:
                    print 'mother ridge index: ', motherind, 'the ridge contributes ', mwtvals.sum(), " and is ", mridge
                totridgewt+=mwtvals.sum()
                ridgelen+=len(mrind) #if a child ridge has a mother that is the child of another mother, the wt and len from this grandmother does not count towards the total of the grandchild
            if verbose:
                print 'ridgelen test', ridgelen, minridgelength, ridgelen>=minridgelength
            if ridgelen>=minridgelength:
                indforlocalmaxtest=(rind>=ridgescalecritind) #if bigger ridge index, smaller wavelet scale (used to be called indforincreasingtest)
                #if (wtvals[indforincreasingtest][1:]>wtvals[indforincreasingtest][:-1]).sum()>0: #if a ridge wt value is bigger than its predecessor(larger scale) then the wt isn't strictly increasing with increasing qscale
                if verbose:
                    print 'the ridge indeces with wave scale less than critical:', indforlocalmaxtest
                    print 'any there test: ', len(wtvals[indforlocalmaxtest])>0
                    if len(wtvals[indforlocalmaxtest])>0:
                        print 'local max test: ', numpy.max(wtvals[indforlocalmaxtest])>=numpy.max(wtvals)
                if len(wtvals[indforlocalmaxtest])>0 and numpy.max(wtvals[indforlocalmaxtest])>=numpy.max(wtvals): #local max is at a scale smaller than critical index - this does nto include mother ridge - the large-scale part of the ridge got to count towards the ridge length
                    if verbose:
                        print 'tot wt test:',  totridgewt, minridgewtsum,  totridgewt>minridgewtsum
                    if totridgewt>minridgewtsum:
                        scaleind=(wt.shape[0]-1-rind[myargmax(wtvals)]) #choose the wt scale and posn at the local maximum of wt - this does not include mother ridges. scaleind is now appropriate for wt (not ridges)
                        posnind=ridge[rind[-1]]#choose the position from the smallest scale in the ridge
                        if motherbool:
                            mother_peaks+=[(count, [scaleind, posnind], family_ridge(ridges, count)[2])]
                        else:
                            peaks+=[[scaleind, posnind]]
                            ridgeind_peaks+=[count]

    ind_potentialpeaks=set(ridgeind_peaks)
    for ind, pk, descendants in mother_peaks:
        ind_potentialpeaks|=set([ind])
    for ind, pk, descendants in mother_peaks:
        if len(ind_potentialpeaks&set(descendants))==0:
            peaks+=[pk]
            if verbose:
                print 'MOTHER RIDGE ',  ind, ' BECOMES PEAK:', pk, '. The non-peak children are indeces ', descendants
        else:
            if verbose:
                print 'MOTHER RIDGE ',  ind, ' NOT A PEAK BECAUSE OF EXISTENCE OF DESCENDANTS: ',  descendants

    return peaks

def motherridgeind_childridge(ridge):#returns None if the ridge has no mother - assumes the ridge is indexed in decreasing order of qscale
    validridgeind=numpy.where((ridge!=32767))[0]
    negridgeind=numpy.where((ridge!=32767)&(ridge<0))[0]
    if len(negridgeind)>0 and negridgeind[0]==validridgeind[0]:#the second condition fails if this ridge is a mother ridge that is not the child of a different ridge
        return -1*ridge[negridgeind[0]]-1
    else:
        return None

def children_ridge(ridges, ind):#returns list of children - assumes the ridge is indexed in decreasing order of qscale
    ridge=ridges[ind]
    mothind=motherridgeind_childridge(ridge)
    if mothind is not None:
        mothset=set([mothind])
    else:
        mothset=set([])
    children=set(numpy.where(ridges==(-1*ind-1))[0])-mothset
    return sorted(list(children))

def family_ridge(ridges, ind):#returns mother (None if the ridge has no mother) and list of children - assumes the ridge is indexed in decreasing order of qscale
    ridge=ridges[ind]
    mothind=motherridgeind_childridge(ridge)

    children=children_ridge(ridges, ind)
    descendants=children
    generation=children
    while len(generation)>0:
        nextgeneration=[]
        for chind in generation:
            nextgeneration+=children_ridge(ridges, chind)
        generation=nextgeneration
        descendants+=nextgeneration

    return mothind,  children, sorted(descendants)

#for testing ridges
#def scale_scalegrid_ind(scalegrid, index='all'):
#    if index=='all':
#        index=numpy.array(range(numpy.uint16(scalegrid[2])), dtype=numpy.float32)
#    elif isinstance(index, list):
#        index=numpy.array(index)
#    return scalegrid[0]*(scalegrid[1]**index)
#import h5py
#
#print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
#h5file=h5py.File('/mnt/SharedData/CHESS2008/2008CHESSh5analysis/dummyJan2010_20081121bsub3RuPtX.dat.h5',mode='r')
#wtgrp=h5file['2/analysis/mar345/wavetrans1d']
##r19=wtgrp['ridges'][19]
##ridges=r19[numpy.array([20])]
#ridges=wtgrp['ridges'][43][:][:]
#qscalegrid=wtgrp.attrs['qscalegrid']
#ridgeqscalevals=scale_scalegrid_ind(qscalegrid)[::-1]
#ridgescalecritind=numpy.where(ridgeqscalevals<=1.2)[0]
#ridgescalecritind=ridgescalecritind[0]
#print perform_peaks_ridges1d(wtgrp['wavetrans'][43,:,:], ridges, ridgescalecritind=ridgescalecritind, minridgelength=100)
#h5file.close()
def Gaussian(pars, x):
    return pars[2]*numpy.exp(-0.5*((x-pars[0])/pars[1])**2)

def Lorentzian(pars, x):#defined in nontraditional way so that pars[2] is the peak height
    return pars[2]/(1+((x-pars[0])/pars[1])**2)

def fitpeakset(qvals, counts, initpars, peakfcn):#peak function must be a function that accepts a list of 3 parameters (the reshape 3 needs to be changed if num params differs)
    numgauss=len(initpars)
    zeroedpeakinds=[]
    repeatwithpkremoved=True #peaks are removed if their fitted height is <0. At the end, these peaks are added to the fit parameter list with 0 height and 0 error
    while repeatwithpkremoved:
        initparscpy=copy.copy(list(initpars))
        for pkind in reversed(zeroedpeakinds):#reverse so opo gets the right index
            initparscpy.pop(pkind)
        if len(initparscpy)==0:
            break
        initparsflat=numpy.float64(initparscpy).flatten()
        def fitfcn(p, x):
            allpars=numpy.reshape(p, (p.size//3, 3))
            if isinstance(x, numpy.ndarray):
                val=numpy.zeros(x.size, dtype='float32')
            else:
                val=0.0
            for pars in allpars:
                val+=peakfcn(pars, x)
            return val
        def residfcn(p, y, x):
            err=y-fitfcn(p, x)
            return err
        counts=numpy.float64(counts)
        qvals=numpy.float64(qvals)
        fitout=scipy.optimize.leastsq(residfcn, initparsflat, args=(counts, qvals), full_output=1)
        if not (fitout[4] in [1, 2]):
            print 'Fitting Error', fitout[4],': ', fitout[3]
        finalparams=numpy.float32(fitout[0])
        finalparamsshaped=numpy.reshape(finalparams, (len(finalparams)//3, 3))
        negpeakinds=numpy.where(finalparamsshaped[:, 2]<0)[0]
        zeroedpeakinds+=list(negpeakinds)
        zeroedpeakinds.sort()
        repeatwithpkremoved=len(negpeakinds)>0
#        print '^^^^^^^^^^^^^^^'
#        print initparsflat
#        print finalparamsshaped
#        pylab.plot(qvals, counts, 'b.')
#        pylab.show()
    if not (fitout[1] is None):
        covmat=fitout[1]
        sigmas=numpy.float32([covmat[i, i] for i in range(len(finalparams))])
    else:
        print 'COVARIANCE NOT CALCULATED:', fitout[4],': ', fitout[3]
        sigmas=numpy.zeros(len(finalparams), dtype='float32')
    finalresid=numpy.sqrt((residfcn(finalparams, qvals, counts)**2).sum())
    #pylab.plot(qvals, counts, 'k.', qvals, fitfcn(finalparams, qvals), 'r-')

    sigmashaped=numpy.reshape(sigmas, (len(finalparams)//3, 3))
    for pkind in zeroedpeakinds:
        finalparamsshaped=list(finalparamsshaped)
        sigmashaped=list(sigmashaped)
        finalparamsshaped.insert(pkind, initpars[pkind][:2]+[0.])
        sigmashaped.insert(pkind, [0., 0., 0.])
        finalparamsshaped=numpy.float64(finalparamsshaped)
        sigmashaped=numpy.float64(sigmashaped)
    return (finalparamsshaped, sigmashaped, finalresid)


def windows_peakpositions(qgrid, qscales, qposns, windowextend_qscales):
    posns=ind_qgrid_q(qgrid, qposns, fractional=True)
    widths=1.0*windowextend_qscales*qscales/qgrid[1]
    #print [[p, w] for p, w in zip(posns, widths)]
    extentsets=[set(range(int(round(p-w)), 1+int(round(p+w)))) for p, w in zip(posns, widths)]
    #print extentsets
    windowsets=[]
    currentset=copy.copy(extentsets[0])
    peakindlists=[]
    currentpeaks=[]
    for i in range(len(extentsets)):
        #if len(currentset&extentsets[i])>0:   this is good enough if later peaks can't extend throught he current peak to previous windows but just in case...
        testset=copy.copy(extentsets[i])
        for j in range(i, len(extentsets)):
            testset|=extentsets[j]
        if len(currentset&testset)>0:
            currentset|=extentsets[i]
            currentpeaks+=[i]
        else:
            windowsets+=[currentset]
            peakindlists+=[currentpeaks]
            currentset=extentsets[i]
            currentpeaks=[i]

    if len(currentset)>0:
        windowsets+=[currentset]
        peakindlists+=[currentpeaks]
    indrangeandpeakinds=tuple([])
    for w, p in zip(windowsets, peakindlists):
        minind=max(min(w), 0)
        maxplusone=min(1+max(w), qgrid[2])
        indrangeandpeakinds+=(([minind, maxplusone], p),)
    return indrangeandpeakinds

def fillgapswithinterp(allindslist, partindslist, partvals, indexinterval_fitinds=8):#allindslist equally spaced and contiguous
    partindsset=set(partindslist)
    partvals=numpy.float32(partvals)
    if 0 in partindslist:
        startinds=[]
    else:
        startinds=[0]
    for i in allindslist[:-1]:
        if (i in partindsset) and not (i+1 in partindsset):
            startinds+=[i+1]

    stopinds=[]
    for i in allindslist[1:]:
        if (i in partindsset) and not (i-1 in partindsset):
            stopinds+=[i-1]
    if not (allindslist[-1] in partindslist):
        stopinds+=[allindslist[-1]]

    fullvals=numpy.zeros(len(allindslist), dtype='float32')
    fullvals[partindslist]=partvals[:]

    for i, j in zip(startinds, stopinds):
        indstofill=numpy.float32(range(i, j+1))
        fitinds=sorted(list(partindsset.intersection(set(range(i-indexinterval_fitinds*(len(indstofill)-3), i, indexinterval_fitinds)+range(j+1, j+1+indexinterval_fitinds*(3+len(indstofill)), indexinterval_fitinds))))) #use range ainstead of allindslist becuase could eb out of range
        fitvals=numpy.float32([partvals[partindslist.index(f)] for f in fitinds])
        fitinds=numpy.float32(fitinds)
        splineorder=min(len(fitinds)-1, 3)
        if splineorder==0:#only one data point to use. can't be no data points to use becuase thie hole has an edge
            fillvals=numpy.float32([fitvals[0]]*len(indstofill))
        else:
            interpfcn=scipy.interpolate.UnivariateSpline(fitinds,fitvals,k=splineorder)
            fillvals=numpy.float32(interpfcn(indstofill))
        fullvals[numpy.uint16(numpy.round(indstofill))]=fillvals[:]
    return fullvals

def stripbadcharsfromnumstr(numstr):
    valchars=[c for c in numstr if c.isdigit() or c=='.' or c=='-']
    return ''.join(valchars)

def cart_comp(comp):
    if isinstance(comp, list) or (isinstance(comp, numpy.ndarray) and comp.ndim==1):
        return [1.-comp[0]-0.5*comp[1], comp[1]]
    else:
        return numpy.float32([1.-comp[:, 0]-0.5*comp[:, 1], comp[:, 1]]).T

def compdistarr_comp(comp):#comp must be array of compositions, each element of comp is supposed to be a 3-array of the fractions
    return numpy.float32([[numpy.sqrt(((a-b)**2).sum()) for b in comp] for a in comp]/numpy.sqrt(2.))

def findcompnieghbors(comp, pointlist=None, critcompdist=.15):#returns a list, the ith element is a list of the indeces of comp the are neighbors of comp[i]. if i is not in pointlist, it does not have neighbors and is noone's neighbor
    comp=numpy.float32(comp)
    if pointlist is None:
        pointlist=range(comp.shape[0])
    pointlist=list(pointlist)
    allind=range(comp.shape[0])
    comp=comp[numpy.uint16(pointlist)]
    finitecompaxes=numpy.where(comp.sum(axis=0)>0.)[0]
    if comp.shape[1]==2 or len(finitecompaxes)<=2:  #binary
        print 'USED SIMPLY BINARY FORMULA FOR NEIGHBORS'
        a=comp[:, finitecompaxes[0]]
        sortind=a.argsort()
        disp=numpy.array([-1, 1], dtype='int16')
        neighbors=[[sortind[j] for j in numpy.where(sortind==i)[0][0]+disp if j>=0 and j<len(pointlist)] for i in range(len(pointlist))]
        neighbors=[sorted(n) for n in neighbors]
    else:
        cart=cart_comp(comp)
        tri=dlny.Triangulation(cart[:, 0], cart[:, 1])
        neighdict=tri.node_graph()
        neighbors=[sorted(list(neighdict[k])) for k in sorted(list(neighdict.keys()))]

    compdist=compdistarr_comp(comp)
    n=[]
    for i in allind:
        if i in pointlist:
            j=pointlist.index(i)
            n+=[[pointlist[ind] for ind in neighbors[j] if compdist[ind, j]<critcompdist]]
        else:
            n+=[[]]
    return n


def findposnnieghbors(xcoords, zcoords, pointlist=None, critdist=999.):#returns a list, the ith element is a list of the indeces of comp the are neighbors of comp[i]. if i is not in pointlist, it does not have neighbors and is noone's neighbor
    xcoords=numpy.float32(xcoords)
    zcoords=numpy.float32(zcoords)
    if pointlist is None:
        pointlist=range(xcoords.shape[0])
    pointlist=list(pointlist)
    allind=range(xcoords.shape[0])
    xcoords=xcoords[numpy.uint16(pointlist)]
    zcoords=zcoords[numpy.uint16(pointlist)]

    tri=dlny.Triangulation(xcoords, zcoords)
    neighdict=tri.node_graph()
    neighbors=[sorted(list(neighdict[k])) for k in sorted(list(neighdict.keys()))]

    dist=numpy.sqrt(numpy.add.outer(xcoords, -1.0*xcoords)**2+numpy.add.outer(zcoords, -1.0*zcoords)**2)
    n=[]
    for i in allind:
        if i in pointlist:
            j=pointlist.index(i)
            n+=[[pointlist[ind] for ind in neighbors[j] if dist[ind, j]<critdist]]
        else:
            n+=[[]]
    return n


def findneighborswithinradius(distarray, critdist, pointlist=None): #distarray should be squre array where i,j is the distance between i and j
    if pointlist is None:
        pointlist=range(distarray.shape[0])
    pointlist=list(pointlist)
    allind=range(distarray.shape[0])

    n=[]

    for i in allind:
        if i in pointlist:
            n+=[[ind for ind in pointlist if distarray[ind, i]<critdist and ind!=i]]
        else:
            n+=[[]]
    return n

def myargmin(a): #this is to resolve the problem I reported in numpy Ticket #1429
    if len(a.shape)>1:
        print 'WARNING: behavior of myargmin not tested for multidimmensional arrays'
    if not numpy.isnan(a[0]):
        return numpy.argmin(a)
    if numpy.min(numpy.isnan(a)):#everything is nan
        return 0
    ind=numpy.argmin(numpy.isnan(a))
    return ind+numpy.argmin(a[ind:])

def myargmax(a): #this is to resolve the problem I reported in numpy Ticket #1429
    if len(a.shape)>1:
        print 'WARNING: behavior of myargmin not tested for multidimmensional arrays'
    if not numpy.isnan(a[0]):
        return numpy.argmax(a)
    if numpy.min(numpy.isnan(a)):#everything is nan
        return 0
    ind=numpy.argmin(numpy.isnan(a))
    return ind+numpy.argmax(a[ind:])
