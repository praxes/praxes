import numpy

from .xrd_math_fcns import *

def eV_nm(wl):
    return 1239.8/wl

def pix_q(q, L,wl, psize=0.1):  #q is scattering vector in 1/nm.  L is detector distance in mm.  wl is wavelength in nm, 0.1mm pixels. return float32 pixel#
    return numpy.float32((1.0*L/psize)*qprime_q(q, wl)*numpy.sqrt(2.0-qprime_q(q, wl)**2)/(1-qprime_q(q, wl)**2))

def rho_q(q, L,wl):
    return pix_q(q, L,wl, psize=1.0)

def twotheta_q(q, wl, units='deg'): #q is scattering vector in 1/nm.  wl is wavelength in nm. return float32 2Theta value in degrees unless units='rad'
    if units=='rad':
        return numpy.float32(2.0*numpy.arcsin(wl*q/(4.0*numpy.pi)))
    else:
        return numpy.float32(2.0*numpy.arcsin(wl*q/(4.0*numpy.pi))*180.0/numpy.pi)

def d_q(q): #q is scattering vector in 1/nm.  wl is wavelength in nm. return float32 2Theta value in degrees unless units='rad'
    return numpy.float32(2.0*numpy.pi/q)

def qprime_q(q, wl):
    return q*numpy.sqrt(2.0)*wl/(4.0*numpy.pi)

def q_qprime(qprime, wl):
    return qprime*(4.0*numpy.pi)/(numpy.sqrt(2.0)*wl)

def qprime_rho(rho,  L):
    return numpy.sqrt(1.0-1.0/numpy.sqrt(1.0+(1.0*rho/L)**2))

def q_rho(rho, L, wl):
    return q_qprime(qprime_rho(rho,  L), wl)

def q_pix(pix, L, wl, psize=0.1):
    return q_rho(pix*psize, L, wl)

def qprime_rhosq(rhosq,  L):
    return numpy.sqrt(1.0-1.0/numpy.sqrt(1.0+(1.0*rhosq/L**2)))

def q_rhosq(rhosq, L, wl):
    return q_qprime(qprime_rhosq(rhosq,  L), wl)

#def realspacesolidangle_q(q, L,wl, psize=0.1):  #gives the solid angle in steradians
#    rho=pix_q(q, L,wl, psize)*psize  #rho in mm
#    return psize*psize*L/(L*L+rho*rho)**1.5

def pixelarearatio_q(q, L,wl, psize=0.1):  #gives the solid angle in steradians
    rho=pix_q(q, L,wl, psize)*psize  #rho in mm
    return L/(L*L+rho*rho)**0.5



def powdersolidangle_q(q, L,wl, psize=0.1, factor=1000000):  #gives the solid angle in steradians. the psize is to give the spatial extent of the pixels and if ave of pixels is done to give 1 effective bigger pixel, this psize need NOT be changed. averaging and then using the original psize is equivalent to summing and using the larger psize.#the 10^6 factor makes the units microsterradians
    rho=pix_q(q, L,wl, psize)*psize  #rho in mm
    return factor*(4*(numpy.pi**2)*(psize**2)/(L*(2.0**0.5)*(wl**2)))*((1-(1+(rho/L)**2)**(-0.5))**0.5)/(rho*(q**2)*(1+(rho/L)**2))

def textureangularcoverage_q(q, L,wl, psize=0.1, factor=1000): #gives the linear of cross section the a pixel covers on the texture ring in recip space.  units are radians. 10^3 factor makes unit milliradians
    qp=qprime_q(q, wl)
    return psize*(1-qp**2)/(1.0*L*qp*numpy.sqrt(2-qp**2))

def q_twotheta(twotheta, wl, units='deg'): #units are those of twotheta, wl in nm, q in 1/nm
    if units=='deg':
        twotheta*=(numpy.pi/180.0)
    return 4*numpy.pi*numpy.sin(twotheta/2.0)/wl



#def chi_q_azim(q, azim, alpharad, L, wl):#azim in rad
#    twoth=twotheta_q(q, wl, 'rad')
#    return numpy.arccos((d_q(q)/wl)*(numpy.cos(alpharad)-numpy.sqrt(1-(numpy.sin(twoth)**2)*numpy.sin(azim)**2)*numpy.cos(alpharad-numpy.arctan(numpy.tan(twoth)*numpy.cos(azim)))))

#def chi_q_azim(q, azim, alpharad, L, wl):#azim in rad
#    mu=2.0*numpy.pi/wl
#    return numpy.arccos((numpy.sin(alpharad)*numpy.cos(azim)+numpy.cos(alpharad)*q/(2*mu))/numpy.sqrt(1+(q/(2*mu))**2))

def azimuth_coords(x,y): #horizontal is y (second index) so azim is zero when y=0, x<0
    nx=-x
    if nx==0:
        return (y!=0)*(numpy.pi/2-numpy.pi*(y<0))
    if nx<0:
        return numpy.pi-numpy.arctan(-1.0*y/nx)
    if y<0:
        return 2.0*numpy.pi-numpy.arctan(-1.0*y/nx)
    return numpy.arctan(y/nx)

def chi_q_azim(q, azim, alpharad, L, wl):#azim in rad
    mu=2.0*numpy.pi/wl
    return numpy.pi-numpy.arccos(numpy.sqrt(1-(q/(2*mu))**2)*numpy.sin(alpharad)*numpy.cos(azim)+numpy.cos(alpharad)*q/(2*mu))

def azim_q_chi(q, chi, alpharad, L, wl):#chi in rad
    mu=2.0*numpy.pi/wl
    #in below line, change cos(chi) to cos(pi-chi)=-cos(chi) per Mar2010 updates....in other calculations there is no change because sin(chi)=sin(pi-chi)
    #return numpy.arccos((numpy.cos(chi)-numpy.cos(alpharad)*q/(2*mu))/(numpy.sqrt(1-(q/(2*mu))**2)*numpy.sin(alpharad)))
    return numpy.arccos((-1.*numpy.cos(chi)-numpy.cos(alpharad)*q/(2*mu))/(numpy.sqrt(1-(q/(2*mu))**2)*numpy.sin(alpharad)))

def dchidazim_q_chi(q, chi, alpharad, L, wl):#azim in rad
    mu=2.0*numpy.pi/wl
    azim=azim_q_chi(q, chi, alpharad, L, wl)
    return numpy.sqrt(1-(q/(2*mu))**2)*numpy.sin(alpharad)*numpy.sin(azim)/numpy.sin(chi)

def dchidazim_q_chi_azim(q, chi, azim, alpharad, L, wl):#azim in rad
    mu=2.0*numpy.pi/wl
    t=numpy.sqrt(1-(q/(2*mu))**2)*numpy.sin(alpharad)*numpy.sin(azim)/numpy.sin(chi)
    print '^^^', numpy.where(numpy.isnan(t))
    return t

def dchidazim_q_azim(q, azim, alpharad, L, wl):#azim in rad
    mu=2.0*numpy.pi/wl
    chi=chi_q_azim(q, azim, alpharad, L, wl)
    return numpy.sqrt(1-(q/(2*mu))**2)*numpy.sin(alpharad)*numpy.sin(azim)/numpy.sin(chi)

def dqdrho_q_rho(q, rho, L, wl):
    qprime=qprime_q(q, wl)
    b=q_qprime(1, wl)
    return 2.0*rho*((1-qprime**2)**3)/(qprime*L*L)

def dqdrho_q(q, L, wl):
    qprime=qprime_q(q, wl)
    rho=rho_q(q, L,wl)
    b=q_qprime(1, wl)
    return 2.0*rho*((1-qprime**2)**3)/(qprime*L*L)

def dchidgamma_q_chi_azim(q, chi, azim, alpharad, wl):#azim in rad
    mu=2.0*numpy.pi/wl
    return numpy.sin(alpharad)*numpy.sin(azim)*numpy.sqrt(1.0-(q/(2.0*mu))**2)/numpy.sin(chi)

def dchidgamma_q_chi(q, chi, alpharad, L, wl):#azim in rad
    azim=azim_q_chi(q, chi, alpharad, L, wl)
    mu=2.0*numpy.pi/wl
    return numpy.sin(alpharad)*numpy.sin(azim)*numpy.sqrt(1.0-(q/(2.0*mu))**2)/numpy.sin(chi)

def dqchiperpixel(q, chi, azim, alpharad, L, wl, binpsize=0.1):
    rho=rho_q(q, L,wl)
    return (binpsize**2)*dqdrho_q(q, L, wl)*dchidgamma_q_chi_azim(q, chi, azim, alpharad, wl)/rho

def polarizfactor_q_twotheta_azim(q, twotheta, azim, wl):
    qprime=qprime_q(q, wl)
    return (1.-(1.-qprime**2.)*(numpy.cos(azim)**2.)*(numpy.sin(twotheta)**2.))*numpy.cos(twotheta)

def Si_atomsensfact(twotheta, wl):#this euqation is empirical fit to textbook data
    x=numpy.sin(twotheta/2.)/wl
    return 1./(7.1393e-002+1.5952e-002*x**1+1.9780e-003*x**2+-1.0921e-003*x**3+2.1368e-004*x**4+-1.0775e-005*x**5)

def scherrersize(q, qfwhm, wl): #in nm if wl in nm, L in mm, q in 1/nm
    tlow=twotheta_q(q-qfwhm/2.0, wl, units='rad')
    thigh=twotheta_q(q+qfwhm/2.0, wl, units='rad')
    t=twotheta_q(q, wl, units='rad')
    return wl/((thigh-tlow)*numpy.cos(t/2.0))

def scherrerqwidth(q, grainsize, wl): #size in grain size in nm
    t=twotheta_q(q, wl, units='rad')
    delt=wl/(grainsize*numpy.cos(t/2.0))
    return q_twotheta(t+delt/2.0, wl, units='rad')-q_twotheta(t-delt/2.0, wl, units='rad')

def q_qgrid_ind(qgrid, index='all'):
    if index=='all':
        index=numpy.array(range(numpy.uint16(qgrid[2])), dtype=numpy.float32)
    elif isinstance(index, list):
        index=numpy.array(index)
    return qgrid[0]+qgrid[1]*index

def qgrid_minmaxint(min, max, inter):
    num=(max-min)//inter+1
    return [min, inter, num]

def qgrid_minmaxnum(min, max, num):
    return [min, (1.0*max-min)/(num-1), num]

def minmaxint_qgrid(qgrid):
    return (qgrid[0], qgrid[0]+qgrid[1]*(qgrid[2]-1), qgrid[1])

def slotends_qgrid(qgrid):
    return numpy.array(range(numpy.uint16(qgrid[2])+1), dtype='float32')*qgrid[1]+qgrid[0]-qgrid[1]/2.0

def ind_qgrid_q(qgrid, q, fractional=True):
    if fractional:
        return (1.0*q-qgrid[0])/qgrid[1]
    else:
        return numpy.int32(numpy.round((1.0*q-qgrid[0])/qgrid[1]))

def bingrid_grid(grid, mapbin=3):
    return [grid[0]+grid[1]*sum(range(mapbin))/(1.0*mapbin), grid[1]*mapbin, int(numpy.ceil(grid[2]/(1.0*mapbin)))]

def xmmzmm_img_xzgrid(img, xgrid, zgrid, mesh=True):
    if isinstance(img, list):
        img=numpy.float32(img)
    if mesh:
        return ((img % xgrid[2])*xgrid[1]+xgrid[0], (img//xgrid[2])*zgrid[1]+zgrid[0])
    else:
        return (img*xgrid[1]+xgrid[0], img*zgrid[1]+zgrid[0])

def specattr_xzgrid(xgrid, zgrid, mesh):
    #'acquisition_time' is not calculated
    specattr={}
    if mesh:
        specattr['acquisition_shape']=(xgrid[2], zgrid[2])
        img=range(xgrid[2]*zgrid[2])
    else:
        specattr['acquisition_shape']=(xgrid[2],)
        img=range(xgrid[2])
    x, z=xmmzmm_img_xzgrid(img, xgrid, zgrid, mesh=mesh)
    specattr['x']=x
    specattr['z']=z
    return specattr

def scale_scalegrid_ind(scalegrid, index='all'):
    if index=='all':
        index=numpy.array(range(numpy.uint16(scalegrid[2])), dtype=numpy.float32)
    elif isinstance(index, list):
        index=numpy.array(index)
    return scalegrid[0]*(scalegrid[1]**index)

def scalegrid_minmaxint(min, max, inter):
    num=int(round(numpy.log(1.0*max/min)/numpy.log(inter)))+1
    return [min, inter, num]

def scalegrid_minmaxnum(min, max, num):
    return [min, numpy.exp(numpy.log(1.0*max/min)/(num-1)), num]

def minmaxint_scalegrid(scalegrid):
    return (scalegrid[0], scalegrid[0]*(scalegrid[1]**(scalegrid[2]-1)), scalegrid[1])

def ind_scalegrid_scale(scalegrid, scale):
    return int(round(numpy.log(1.0*scale/scalegrid[0])/numpy.log(scalegrid[1])))

def centerindeces_fit2dcenter(centerlist, detsize=3450):
    #centerlist can be 2 elements or longer, the 2 being the horizontal and vertical beam cetner from fit2d (where the origing is 1,1)
    return [(detsize-1)-(centerlist[1]-1), centerlist[0]-1]

def bincenterind_centerind(center, bin): #center is the center in array indeces (not fit2d). if initsizey is None then assume square. not necessarilt int
    if bin>1:
        center=center[0:2]
        bincenter=[]
        for c in center:
            newbin=(c+1.0/bin)%bin
            bincenter+=[newbin+(c-bin*newbin-(bin-1.0)/2.0)/bin]
        return bincenter
    else:
        return center[0:2]

def scaleposngrid_affinegrid(affinegrid):
    scales=scale_scalegrid_ind(affinegrid[:3])
    return [[sc, qgrid_minmaxint(affinegrid[3], affinegrid[4], 1.0*sc/affinegrid[5])] for sc in scales]

def scaleposnlist_affinegrid(affinegrid):
    t=scaleposngrid_affinegrid(affinegrid)
    posnlist=[list(q_qgrid_ind(dup[1])) for dup in t]
    scalelist=[[dup[0]]*len(posns) for dup, posns in zip(t, posnlist)]
    return numpy.array(zip(flatten(scalelist), flatten(posnlist)))

def tiltdirectionoperation(center, imageshape, tiltdir='bottom'):
    transbool=(tiltdir=='right' or tiltdir=='left')
    invbool=(tiltdir=='top' or tiltdir=='left')
    if transbool:
        center=center[::-1]
        imageshape=imageshape[::-1]
    if invbool:
        center[0]=imageshape[0]-1-center[0]
    return center, imageshape

def tiltdirectioninverseoperation(image, tiltdir):
    transbool=(tiltdir=='right' or tiltdir=='left')
    invbool=(tiltdir=='top' or tiltdir=='left')
    if transbool:
        image=numpy.transpose(image)
    if invbool:
        image=image[::-1, :]
    return image

delQ_1mmbeam=lambda q,L,wl:q_rho(rho_q(q, L,wl)+1.,L,wl)-q

delQ_1pixel=lambda q,L,wl:q_pix(pix_q(q, L,wl, psize=0.2)+1.,L,wl, psize=0.2)-q  #DEFAULT IS SET FOR GE DETECTOR

delQ_1mmL=lambda q,L,wl:q_rho(rho_q(q, L+1.,wl),L+1.,wl)-q_rho(rho_q(q, L,wl),L,wl)
